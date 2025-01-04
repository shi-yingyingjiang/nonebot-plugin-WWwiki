# coding=utf-8
import json
import httpx

from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot import on_command

from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import get_link
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template

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

html_spath = get_template("archives")

archive_cards = on_command('鸣潮角色档案')


@archive_cards.handle()
async def _(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await get_link(role_name, listdata)
    if role_id is None:
        await archive_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        roledata = {
            'id': role_id
        }
        async with httpx.AsyncClient() as client:
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            besicinfo = get_basic_information(data)
            data_content = data['data']['content']['modules'][3]['components'][0]['content']

            Data = {
                'roleimg': besicinfo.get('role_img'),
                'rolename': besicinfo.get('role_name'),
                'roledescription': besicinfo.get('role_description'),
                'roledescriptiontitle': besicinfo.get('role_description_title'),
                'content': data_content,
            }

            archive_card = await draw_main(
                Data,
                html_spath.name,
                html_spath.parent.as_posix(),
            )

    await UniMessage.image(raw=archive_card).finish()
