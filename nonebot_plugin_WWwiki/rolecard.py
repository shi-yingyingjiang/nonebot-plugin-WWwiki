import json
import httpx
import os
from nonebot import on_command
from .itemlink import Get_link
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .model import Model
from io import StringIO
from pandas import read_html
import json
from jinja2 import Template
from playwright.async_api import async_playwright
from io import BytesIO
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg







headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests' : '1',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Ch-Ua' : '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Wiki_type' : '9'

}

listdata = {
    'catalogueId': '1105',
    'page': '1',
    'limit': '1000'
    }

html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'rolecard', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'rolecard', 'out_page.html')
character_cards = on_command('鸣潮角色查询')


@character_cards.handle()
async def role_data(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_link(role_name, listdata)
    if role_id ==None:
        await character_cards.finish(f'没有找到角色,错误参数：' +  role_name)
    else:
        roledata = {
            'id' : role_id
        }
        async with httpx.AsyncClient() as client:
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            besicinfo = get_basic_information(data)
            model = Model.parse_raw(roledata_r.text)
            otherinfo = read_html(StringIO(model.data.content.modules[0].components[1].content))
            character_statistics = read_html(StringIO(model.data.content.modules[0].components[2].tabs[7].content))
            df = otherinfo[0]
            data_dict = df.set_index(df.columns[0])[df.columns[1]].to_dict()
            my_dict = data_dict

            def get_value_from_dict(dictionary, key):
                return dictionary.get(key, "未知")
            

            otherinfo_dict = {
                'identity': get_value_from_dict(my_dict, '身份'),
                'affiliation' : get_value_from_dict(my_dict, '所属'),
                'specialcuisine': get_value_from_dict(my_dict, '特殊料理'),
                'zhcv': get_value_from_dict(my_dict, '中文CV'),
                'jpcv': get_value_from_dict(my_dict, '日文CV'),
                'encv': get_value_from_dict(my_dict, '英文CV'),
                'kocv': get_value_from_dict(my_dict, '韩文CV'),
                'version': get_value_from_dict(my_dict, '实装版本')
            }

            Data = {
                'roleimg' : besicinfo.get('role_img'),
                'roleenname' : besicinfo.get('role_en_name'),
                'roleDescription' : besicinfo.get('role_description'),
                'roleDescriptiontitle' : besicinfo.get('role_description_title'),
                'campIcon': besicinfo.get('campIcon'),
                'title': besicinfo.get('role_name'),
                'attribute' : besicinfo.get('attribute'),
                'birthplace' : besicinfo.get('birthplace'),
                'weapon' : besicinfo.get('weapon'),
                'gender' : besicinfo.get('role_gender'),
                'identity' : otherinfo_dict.get('identity'),
                'affiliation' : otherinfo_dict.get('affiliation'),
                'specialcuisine' : otherinfo_dict.get('specialcuisine'),
                'zhcv' : otherinfo_dict.get('zhcv'),
                'jpcv' : otherinfo_dict.get('jpcv'),
                'encv' : otherinfo_dict.get('encv'),
                'kocv' : otherinfo_dict.get('kocv'),
                'version' : otherinfo_dict.get('version'),
                'baselife' : character_statistics[0][1][1],
                'basicattack' : character_statistics[0][1][2],
                'basicdefense' : character_statistics[0][1][3],

            }

            with open(html_spath, 'r', encoding='utf-8') as f:
                template_str = f.read()
            page_template = Template(template_str)
            page_html = page_template.render(Data)
            with open(out_html_path, 'w', encoding='utf-8') as f:
                f.write(page_html)

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(out_html_path)

                # 截取全屏截图
                role_card = BytesIO(await page.screenshot(full_page=True))

                # 关闭页面、上下文和浏览器
                await page.close()
                await context.close()
                await browser.close()
    await character_cards.finish(MessageSegment.image(role_card))

