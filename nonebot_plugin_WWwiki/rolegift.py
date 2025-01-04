# coding=utf-8
import json
import httpx

from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot import on_command

from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import get_link
from .getarchives import get_gift
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template

html_spath = get_template("gift")

gift_cards = on_command('鸣潮珍贵之物')

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
    'catalogueId': '1105',
    'page': '1',
    'limit': '1000'
}


@gift_cards.handle()
async def giftcard(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await get_link(role_name, listdata)
    if role_id is None:
        await gift_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        async with httpx.AsyncClient() as client:
            roledata = {
                'id': role_id
            }
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            info_data = get_basic_information(data)
            gift_one_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[0].get(
                'content')
            gift_one = get_gift(gift_one_data)
            gift_two_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[1].get(
                'content')
            gift_two = get_gift(gift_two_data)
            gift_three_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[2].get(
                'content')
            gift_three = get_gift(gift_three_data)
            gift_four_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[3].get(
                'content')
            gift_four = get_gift(gift_four_data)

            Data = {
                'roleimg': info_data.get('role_img'),
                'rolename': info_data.get('role_name'),
                'roledescription': info_data.get('role_description'),
                'roledescriptiontitle': info_data.get('role_description_title'),
                'giftimgo': gift_one.get('giftimg'),
                'gifttitleo': gift_one.get('gifttitle'),
                'giftcontento': gift_one.get('giftcontent'),
                'giftimg2': gift_two.get('giftimg'),
                'gifttitle2': gift_two.get('gifttitle'),
                'giftcontent2': gift_two.get('giftcontent'),
                'giftimg3': gift_three.get('giftimg'),
                'gifttitle3': gift_three.get('gifttitle'),
                'giftcontent3': gift_three.get('giftcontent'),
                'giftimg4': gift_four.get('giftimg'),
                'gifttitle4': gift_four.get('gifttitle'),
                'giftcontent4': gift_four.get('giftcontent'),
            }

            skll_image = await draw_main(
                Data,
                html_spath.name,
                html_spath.parent.as_posix(),
            )

        await UniMessage.image(raw=skll_image).finish()
