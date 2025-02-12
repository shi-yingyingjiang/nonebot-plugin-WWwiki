# coding=utf-8
import httpx
import json
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot import on_command
from bs4 import BeautifulSoup
from .itemlink import get_link,classify
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template

enemy_cards = on_command('鸣潮敌人查询')

getentrydetail = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Wiki_type': '9'

}

enemy = {
    'catalogueId': '1158',
    'page': '1',
    'limit': '1000'
}


drops = '''<table style="width: 70%;height: 215px;">
                    <tr>
                        <td>
                            <p><img src="{material_img}" alt="" style="width: 96px;"></p>
                            <p>{material_name}</p>
                        </td>
                        <td>
                            <p><img src="{echo_img}" alt="" style="width: 96px;"></p>
                            <p>{echo_name}</p>
                        </td>
                    </tr>
                </table>'''

classandlevel = '''<table style="width: 30%; height: 215px;border-collapse: collapse;">
                    <tr>
                        <td>种类</td>
                        <td>级别</td>
                    </tr>
                    <tr>
                        <td>{class_text}</td>
                        <td>{level_text}</td>
                    </tr>
                </table>'''


def resistance(html):# 抗性数据
    soup = BeautifulSoup(html, 'html.parser')
    data_list = soup.find_all('tr')
    vale_data = []
    for i in range(1,8):
        trs = data_list[i]
        data_td = trs.find_all('td')
        valedata = data_td[1].text
        vale_data.append(valedata)
    
    return vale_data

def defense(html,html1):#防御的数据 level80 100
    soup = BeautifulSoup(html, 'html.parser')
    soup1 = BeautifulSoup(html1, 'html.parser')
    defense_tr = soup.find_all('tr')[0]
    defense = defense_tr.find_all('td')[1].text
    defense_tr1 = soup1.find_all('tr')[0]
    defense1 = defense_tr1.find_all('td')[1].text

    return defense, defense1


resistance_template = '''
                {rankingbody}
                <table style="width: 100%;border-collapse: collapse;">
                <colgroup>
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                    <col style="width: 12.5%;">
                </colgroup>
                <tr><td>防御</td><td>物理抗性</td><td style="color: rgb(53,152,219);">冷凝抗性</td><td style="color: rgb(224,62,45);">热熔抗性</td><td style="color: rgb(241,196,15);">衍射抗性</td><td style="color: rgb(132,63,161);">湮灭抗性</td><td style="color: rgb(22,145,121);">气动抗性</td><td style="color: rgb(185,106,217);">导电抗性</td></tr>
                <tr><<td>{fangyu}</td><td>{wuli}</td><td>{lengning}</td><td>{rerong}</td><td>{yanshe}</td><td>{yanmie}</td><td>{qidong}</td><td>{daodian}</td></tr>
            </table>'''



def make_data_table(html,html1,ranking_body):
    rankingbody = ranking_body
    defense_data = defense(html,html1)#防御的数据 level80 100 ,一个列表
    resistance_data = resistance(html)# 抗性数据 , 一个列表
    fangyu = defense_data[1] + '(80级)' + '<br>' + defense_data[0] + '(100级)'
    wuli = resistance_data[0]
    lengning = resistance_data[1]
    rerong = resistance_data[2]
    yanshe = resistance_data[3]
    yanmie = resistance_data[4]
    qidong = resistance_data[5]
    daodian = resistance_data[6]
    data_table = resistance_template.format(rankingbody=rankingbody,fangyu=fangyu, wuli=wuli, lengning=lengning, rerong=rerong, yanshe=yanshe, yanmie=yanmie, qidong=qidong, daodian=daodian)

    return data_table


html_spath = get_template("enemy")
classify_spath = get_template("classify")

@enemy_cards.handle()
async def _(args: Message = CommandArg()):
    name = args.extract_plain_text()
    enemy_id = await get_link(name, enemy)
    if enemy_id is None:
        await enemy_cards.finish('没有找到该敌人')
    else:
        enemy_data = {
            'id': enemy_id
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(getentrydetail, data=enemy_data, headers=headers)
            data = json.loads(r.text)
            components = data['data']['content']['modules'][0]['components']
            table1 = components[0]['content']
            soup = BeautifulSoup(table1, 'html.parser')
            tr_list = soup.find_all('tr')
            enemyimg = tr_list[0].find('img')['src']


            tr_description = tr_list[-1]
            description_divs = tr_description.find_all('div')
            identity = description_divs[0].text#身份
            appraise_text = ''.join(str(tag) if tag.name == 'br' else tag for tag in description_divs[1].contents)#简评

            td_drops = tr_list[-3].find_all('td')

            #掉落物的数据
            if len(td_drops) == 2:
                td_material = td_drops[0]
                material_img = td_material.find('img')['src']
                material_name = td_material.find('a').text
                td_echo = td_drops[1]
                echo_img = td_echo.find('img')['src']
                echo_name = td_echo.find('a').text
                drops_html = drops.format(material_img=material_img, material_name=material_name, echo_img=echo_img, echo_name=echo_name)
            else:   #特例；残星会等不会掉落声骸的人类敌人
                td_material = td_drops[0]
                material_img = td_material.find('img')['src']
                material_name = td_material.text
                echo_img = ''
                echo_name = ''
                drops_html = drops.format(material_img=material_img, material_name=material_name, echo_img=echo_img, echo_name=echo_name)

            #判断是否存在种类级别，以及返回数据
            if len(tr_list) == 7:
                tr_class = tr_list[1]
                tr_level = tr_list[2]
                class_text = tr_class.find_all('td')[1].text
                level_text = tr_level.find_all('td')[1].text
                class_level_html = classandlevel.format(class_text=class_text, level_text=level_text)
                diaoluowu = class_level_html + drops_html
            else:
                diaoluowu = drops_html


            


            data_table_data = ''


            # for i in range(1,len(components)):
            #     component = components[i]
            #     html = component['tabs'][-1]['content']
            #     html1 = component['tabs'][-3]['content']
            #     data_table = make_data_table(html,html1)
            #     data_table_data += data_table
            ch = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
            if len(components) > 2:
                n = 1
                for i in range(1,len(components)):
                    ranking = ch[n]
                    ranking_body = ''
                    ranking_template = '''<div style="padding: 25px;">{ranking}阶段</div>'''
                    ranking_body += ranking_template.format(ranking=ranking)
                    component = components[i]
                    html = component['tabs'][-1]['content']
                    html1 = component['tabs'][-3]['content']
                    data_table = make_data_table(html,html1,ranking_body)
                    data_table_data += data_table
                    n += 1
            else:
                html = components[1]['tabs'][-1]['content']
                html1 = components[1]['tabs'][-3]['content']
                ranking_body = ''
                data_table_data = make_data_table(html,html1,ranking_body)
            
            for a_tag in soup.find_all('a'):
                del a_tag['href']

            Data = {
                'enemyimg': enemyimg,
                'name': name,
                'identity': identity,
                'appraise':appraise_text,
                'diaoluowu': diaoluowu,
                'datatabledata': data_table_data
            }

            enemy_card = await draw_main(
                Data,
                html_spath.name,
                html_spath.parent.as_posix(),
            )

    await UniMessage.image(raw=enemy_card).finish()





caseify = on_command("鸣潮掉落物查询",aliases={'鸣潮掉落物'})

@caseify.handle()
async def _(args: Message = CommandArg()):
    thetitle = args.extract_plain_text()
    results,title = await classify(thetitle, enemy)
    if results is None:
        await caseify.finish('没有找到该分类，请重试输入以下分类:\n' + title)
        
    else:
        template = """
        <div class="class">
            <img src="{img}" class="classimg">
            <h1 class="name">{title}</h1> </div>
            """


        html_content = ""

        for item in results:
            img_url = item['contentUrl']
            title = item['title']
            html_content += template.format(img=img_url, title=title)

        Data = {
            'title': thetitle,
            'content': html_content
        }

        classify_card = await draw_main(
            Data,
            classify_spath.name,
            classify_spath.parent.as_posix(),
        )

    await UniMessage.image(raw=classify_card).finish()