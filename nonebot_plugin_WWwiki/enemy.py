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
            table1 = data['data']['content']['modules'][0]['components'][0]['content']
            table2 = data['data']['content']['modules'][0]['components'][1]['tabs'][0]['content']
            soup = BeautifulSoup(table1, 'html.parser')
            for a_tag in soup.find_all('a'):
                del a_tag['href']

            Data = {
                'table1': soup,
                'table2': table2
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