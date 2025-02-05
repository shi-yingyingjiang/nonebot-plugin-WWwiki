import json
from bs4 import BeautifulSoup
from jinja2 import Template
from nonebot import on_command
from nonebot.adapters import Message
import httpx
from nonebot.params import CommandArg
from .util import UniMessage, get_template,template_to_pic
from .judgmentrolename import judgment_role_name
from .itemlink import get_link
from .recommendation import recommendationcards





html_spath = get_template("yituliu")


def make_html(tabs):
    html = ""
    for index, item in enumerate(tabs):
        content = item['content']
        if index < len(tabs) - 1:
            html += content + '\n'
        else:
            html += content
        
    return html

def make_team_html(tabs):
    html_output = ""
    for i, tab in enumerate(tabs):
        if i != 0:
            html_output += f"<span class=\"team\">{tab['title']}</span>\n"
            html_output += tab['content']
            if i < len(tabs) - 1:  # 如果不是最后一个元素，则添加换行
                html_output += "\n"
        else:
            html_output += tab['content']
        

    return html_output


# with open('yituliu.json', 'r', encoding='utf-8') as f:
#     yituliudata = json.load(f)

# components = yituliudata['data']['content']['modules'][0]['components']


# style = components[1]['content']
# material = components[2]['content']
# mechanism = make_html(components[3]['tabs'])
# equipments = make_html(components[4]['tabs'])
# weapon_d = make_html(components[5]['tabs'])
# team = make_team_html(components[6]['tabs'])

# information = components[0]['role']
# roleimg = information['figures'][0]['url']
# introduce = information['roleDescription']
# enname = information['subtitle']
# rolename = information['title']
# ability = ''
# for item in information['info']:
#     if '伤害' in item['text']or '定位' in item['text']:
#         ability += item['text'].split('：')[1] + ' '





# # 解析HTML
# soup = BeautifulSoup(weapon_d, 'html.parser')

# # 去除所有a标签的href属性
# for a_tag in soup.find_all('a'):
#     del a_tag['href']

# # 输出修改后的HTML
# weapon = str(soup)






# Data = {
#     'roleimg': roleimg,
#     'introduce': introduce,
#     'enname': enname,
#     'rolename': rolename,
#     'ability': ability,
#     'style': style,
#     'material': material,
#     'mechanism': mechanism,
#     'equipment': equipments,
#     'weapon': weapon,
#     'team': team
# }


# with open('nrolecard.html', 'r', encoding='utf-8') as f:
#     template_str = f.read()
# page_template = Template(template_str)
# page_html = page_template.render(Data)
# with open('nrolecardout.html', 'w', encoding='utf-8') as f:
#     f.write(page_html)


yituliu_cards = on_command('鸣潮一图流')



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Wiki_type': '9'

}
relist = {
    'catalogueId': '1323',
    'page': '1',
    'limit': '1000'
}
listdata = {
    'catalogueId': '1105',
    'page': '1',
    'limit': '1000'
}


relink = 'https://api.kurobbs.com/wiki/core/catalogue/item/getPage'
EntryDetail = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'

yituliu_cards.handle()
async def yituliucards(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await get_link(role_name, listdata)
    if role_id is None:
        await yituliu_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        rename = role_name+"角色攻略"

        async with httpx.AsyncClient() as client:
            rerole_r = await client.post(relink, data=relist, headers=headers)
            rerole_list = json.loads(rerole_r.text)
            rerecord = rerole_list['data']['results']['records']
            for item in rerecord:
                if rename != item['name']:
                    await yituliu_cards.send(f'该角色暂无一图流,将发送养成推荐')
                    await recommendationcards(args)

                else:
                    entryid = item['content']['linkConfig']['entryId']
                    redata = {
                        'id' : entryid
                    }

                    redata_r = await client.post(EntryDetail, data=redata, headers=headers)
                    redata_data = json.loads(redata_r.text)
                    components = redata_data['data']['content']['modules'][0]['components']
                    style = components[1]['content']
                    material = components[2]['content']
                    mechanism = make_html(components[3]['tabs'])
                    equipments = make_html(components[4]['tabs'])
                    weapon_d = make_html(components[5]['tabs'])
                    team = make_team_html(components[6]['tabs'])

                    information = components[0]['role']
                    roleimg = information['figures'][0]['url']
                    introduce = information['roleDescription']
                    enname = information['subtitle']
                    rolename = information['title']
                    ability = ''
                    for item in information['info']:
                        if '伤害' in item['text']or '定位' in item['text']:
                            ability += item['text'].split('：')[1] + ' '





                    # 解析HTML
                    soup = BeautifulSoup(weapon_d, 'html.parser')

                    # 去除所有a标签的href属性
                    for a_tag in soup.find_all('a'):
                        del a_tag['href']

                    # 输出修改后的HTML
                    weapon = str(soup)






                    Data = {
                        'roleimg': roleimg,
                        'introduce': introduce,
                        'enname': enname,
                        'rolename': rolename,
                        'ability': ability,
                        'style': style,
                        'material': material,
                        'mechanism': mechanism,
                        'equipment': equipments,
                        'weapon': weapon,
                        'team': team
                    }





                    img = await template_to_pic(
                        html_spath.parent.as_posix(),
                        html_spath.name,
                        Data,
                    )


                    await UniMessage.image(raw=img).finish()