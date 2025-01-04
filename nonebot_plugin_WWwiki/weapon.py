# coding=utf-8
import json
import httpx

from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot import on_command
from bs4 import BeautifulSoup

from .itemlink import get_link
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template


weapon_cards = on_command('鸣潮武器查询')

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
    'catalogueId': '1106',
    'page': '1',
    'limit': '1000'
}

html_spath = get_template("weapon")


@weapon_cards.handle()
async def get_weapon_data(args: Message = CommandArg()):
    name = args.extract_plain_text()
    weapon_id = await get_link(name, listdata)
    if weapon_id is None:
        await weapon_cards.finish('没有找到武器,错误参数：' + name)
    else:
        weapondata = {
            'id': weapon_id,
        }
        async with httpx.AsyncClient() as client:
            weapon_r = await client.post(getentrydetail, headers=headers, data=weapondata)
            data = json.loads(weapon_r.text)
            basis = data['data']['content']['modules'][0]['components'][0]['content']
            description = data['data']['content']['modules'][0]['components'][1]['content']
            numeric_value = data['data']['content']['modules'][0]['components'][2]['tabs'][7]['content']

            soup1 = BeautifulSoup(basis, 'html.parser')
            img = soup1.find('img')['src']
            tr2 = soup1.find_all('tr')[1]
            td2 = tr2.find_all('td')[1]
            name = td2.text.strip()

            soup2 = BeautifulSoup(numeric_value, 'html.parser')
            tr2 = soup2.find_all('tr')[1]
            td2 = tr2.find_all('td')[0]
            attribute1 = td2.find_all('p')[0].text.strip()
            attribute2 = td2.find_all('p')[1].text.strip()

            Data = {
                'weaponimg': img,
                'weaponname': name,
                'attribute1': attribute1,
                'attribute2': attribute2,
                'description': description,
            }

            weapon_card = await draw_main(
                Data,
                html_spath.name,
                html_spath.parent.as_posix(),
            )

        await UniMessage.image(raw=weapon_card).finish()
