# coding=utf-8
import json
import httpx
from io import StringIO
from pandas import read_html
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .config import plugin_config
from .itemlink import get_link
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .pil_draw.draw import draw_main
from .util import UniMessage, get_template, template_to_pic


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

html_spath = get_template("rolecard")
character_cards = on_command('鸣潮角色查询')


@character_cards.handle()
async def role_data(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await get_link(role_name, listdata)
    if role_id is None:
        await character_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        roledata = {
            'id': role_id
        }
        async with httpx.AsyncClient() as client:
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            besicinfo = get_basic_information(data)
            # model = type_validate_json(Model, roledata_r.text)
            components=data['data']['content']['modules'][0]['components']
            other_component = next((r for r in components if r.get('title') == '其他信息'),None)
            other_component = next((r for r in components if r.get('title') == '角色统计'),None)

            if other_component:
                otherinfo_content=other_component['content']
            if other_component:
                character_statistics_content=other_component['tabs'][7]['content']
            otherinfo = read_html(StringIO(otherinfo_content))
            character_statistics = read_html(StringIO(character_statistics_content))
            df = otherinfo[0]
            data_dict = df.set_index(df.columns[0])[df.columns[1]].to_dict()
            my_dict = data_dict


            # 获取战斗风格数据
            fighting_style_content = data.get('data').get('content').get('modules')[0].get('components')[3].get('content')

            def get_value_from_dict(dictionary, key):
                return dictionary.get(key, "未知")

            otherinfo_dict = {
                'identity': get_value_from_dict(my_dict, '身份'),
                'affiliation': get_value_from_dict(my_dict, '所属'),
                'specialcuisine': get_value_from_dict(my_dict, '特殊料理'),
                'zhcv': get_value_from_dict(my_dict, '中文CV'),
                'jpcv': get_value_from_dict(my_dict, '日文CV'),
                'encv': get_value_from_dict(my_dict, '英文CV'),
                'kocv': get_value_from_dict(my_dict, '韩文CV'),
                'version': get_value_from_dict(my_dict, '实装版本')
            }

            Data = {
                'roleimg': besicinfo.get('role_img'),
                'roleenname': besicinfo.get('role_en_name'),
                'roleDescription': besicinfo.get('role_description'),
                'roleDescriptiontitle': besicinfo.get('role_description_title'),
                'campIcon': besicinfo.get('campIcon'),
                'title': besicinfo.get('role_name'),
                'attribute': besicinfo.get('attribute'),
                'attributevalue': besicinfo.get('attribute').split('：')[1],
                'birthplace': besicinfo.get('birthplace'),
                'birthplacevalue': besicinfo.get('birthplace').split('：')[1],
                'weapon': besicinfo.get('weapon'),
                'weaponvalue': besicinfo.get('weapon').split('：')[1],
                'gender': besicinfo.get('role_gender'),
                'gendervalue': besicinfo.get('role_gender').split('：')[1],
                'identity': otherinfo_dict.get('identity'),
                'affiliation': otherinfo_dict.get('affiliation'),
                'specialcuisine': otherinfo_dict.get('specialcuisine'),
                'zhcv': otherinfo_dict.get('zhcv'),
                'jpcv': otherinfo_dict.get('jpcv'),
                'encv': otherinfo_dict.get('encv'),
                'kocv': otherinfo_dict.get('kocv'),
                'version': otherinfo_dict.get('version'),
                'baselife': character_statistics[0][1][1],
                'basicattack': character_statistics[0][1][2],
                'basicdefense': character_statistics[0][1][3],
                'promotion': character_statistics[0][3][0],
                'promotionvalue': character_statistics[0][4][0],
                'criticaldamage': character_statistics[0][4][1],
                'bonus': character_statistics[0][3][2],
                'bonusvalue': character_statistics[0][4][2],
                'energy': character_statistics[0][4][3],
                'criticalstrikechance': character_statistics[0][1][4],
                'injurycategory': character_statistics[0][3][4],
                'combat_data': character_statistics[0],
                'fighting_style_content': fighting_style_content
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
