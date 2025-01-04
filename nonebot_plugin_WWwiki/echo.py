# coding=utf-8
import httpx
import json

from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot import on_command
from bs4 import BeautifulSoup

from .itemlink import get_link
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template

echos = on_command('鸣潮声骸查询', aliases={'声骸查询'})

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

listdata = {
    'catalogueId': '1107',
    'page': '1',
    'limit': '1000'
}

html_spath = get_template("echo")


@echos.handle()
async def _(args: Message = CommandArg()):
    name = args.extract_plain_text()
    echo_id = await get_link(name, listdata)
    if echo_id is None:
        await echos.finish('没有找到该声骸')
    else:
        echodata = {'id': echo_id}
        async with httpx.AsyncClient() as client:
            res = await client.post(getentrydetail, data=echodata, headers=headers)
            data = json.loads(res.text)
            img_content = data['data']['content']['modules'][0]['components'][0]['content']
            soup = BeautifulSoup(img_content, 'html.parser')
            img = soup.find('img')
            name = data['data']['name']
            src = img['src']
            info = data['data']['content']['modules'][0]['components'][1]['content']
            skll = data['data']['content']['modules'][0]['components'][2]['tabs'][0]['content']

            Data = {
                'name': name,
                'img': src,
                'info': info,
                'skll': skll
            }

            echo_card = await draw_main(
                Data,
                html_spath.name,
                html_spath.parent.as_posix(),
            )

        await UniMessage.image(raw=echo_card).finish()
