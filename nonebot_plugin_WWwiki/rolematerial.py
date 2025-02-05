# coding=utf-8
import json
import httpx

from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot import on_command

from .getmaterial import (
    # getelementarymaterials,
    # getintermediatematerials,
    # getseniormaterials,
    # getultimatematerials,
    # getskillmaterials,
    role_breakthrough,
    skill_breakthrough
)
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import get_link
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template, template_to_pic
from .config import plugin_config


material_cards = on_command("鸣潮突破材料")

html_spath = get_template("materialcard")

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


@material_cards.handle()
async def _(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await get_link(role_name, listdata)
    if role_id is None:
        await material_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        async with httpx.AsyncClient() as client:
            roledata = {
                'id': role_id
            }
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)

            # elementary_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[
            #     0].get('content')
            role_breakthrough_data = data['data']['content']['modules'][1]['components'][2]['tabs'][5]['content']
            skill_breakthrough_data = data['data']['content']['modules'][1]['components'][3]['tabs'][0]['content']
            # intermediate_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[
            #     1].get('content')
            # senior_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[3].get(
            #     'content')
            # ultimate_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[
            #     5].get('content')
            # skll_material = data.get('data').get('content').get('modules')[1].get('components')[3].get('tabs')[0].get(
            #     'content')
            besicinfo = get_basic_information(data)
            # elementary_material = getelementarymaterials(elementary_material)
            # intermediate_material = getintermediatematerials(intermediate_material)
            # senior_material = getseniormaterials(senior_material)
            # ultimate_material = getultimatematerials(ultimate_material)
            # skll_material = getskillmaterials(skll_material)
            rolebreakthrough = role_breakthrough(role_breakthrough_data)
            skillbreakthrough = skill_breakthrough(skill_breakthrough_data)

            Data = {
                "rolename": besicinfo.get('role_name'),
                'roleimg': besicinfo.get('role_img'),
                'roledescriptiontitle': besicinfo.get('role_description_title'),
                'roledescription': besicinfo.get('role_description'),
                'elementarytitle': skillbreakthrough[0][1],
                'elementaryimg': skillbreakthrough[0][0],
                'intermediatetitle': skillbreakthrough[2][1],
                'intermediateimg': skillbreakthrough[2][0],
                'seniortitle': skillbreakthrough[4][1],
                'seniorimg': skillbreakthrough[4][0],
                'ultimatetitle': skillbreakthrough[6][1],
                'ultimateimg': skillbreakthrough[6][0],
                'footagetitle': rolebreakthrough[0][1],
                'footageimg': rolebreakthrough[0][0],
                'universaltitle': rolebreakthrough[1][1],
                'universalimg': rolebreakthrough[1][0],
                'elementarymaterialtitle': skillbreakthrough[1][1],
                'elementarymaterialimg': skillbreakthrough[1][0],
                'intermediatematerialtitle': skillbreakthrough[3][1],
                'intermediatematerialimg': skillbreakthrough[3][0],
                'seniormaterialtitle': skillbreakthrough[5][1],
                'seniormaterialimg': skillbreakthrough[5][0],
                'ultimatematerialtitle': skillbreakthrough[7][1],
                'ultimatematerialimg': skillbreakthrough[7][0],
                'extratitle': skillbreakthrough[8][1],
                'extraimg': skillbreakthrough[8][0],
            }

            if plugin_config.makeimg_mode == 'htmltopic':
                img = await template_to_pic(
                    html_spath.parent.as_posix(),
                    html_spath.name,
                    Data,
                )
            elif plugin_config.makeimg_mode == 'piltopic':
                img = await draw_main(
                    Data,
                    html_spath.name,
                    html_spath.parent.as_posix(),
                )

        await UniMessage.image(raw=img).finish()
