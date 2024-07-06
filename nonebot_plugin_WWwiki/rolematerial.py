from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command
from .getmaterial import getelementarymaterials,getintermediatematerials,getseniormaterials,getultimatematerials,getskillmaterials
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import Get_link
import httpx
from io import BytesIO
import os
import json
from jinja2 import Template




material_cards = on_command("鸣潮突破材料")


html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'materialcard', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'materialcard', 'out_page.html')




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

@material_cards.handle()
async def _(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_link(role_name,listdata)
    if role_id ==None:
        await material_cards.finish(f'没有找到角色,错误参数：' +  role_name)
    else:
        async with httpx.AsyncClient() as client:
            roledata = {
                'id' : role_id
            }
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)

            elementary_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[0].get('content')
            intermediate_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[1].get('content')
            senior_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[3].get('content')
            ultimate_material = data.get('data').get('content').get('modules')[1].get('components')[2].get('tabs')[5].get('content')
            skll_material = data.get('data').get('content').get('modules')[1].get('components')[3].get('tabs')[0].get('content')
            besicinfo = get_basic_information(data)
            elementary_material = getelementarymaterials(elementary_material)
            intermediate_material = getintermediatematerials(intermediate_material)
            senior_material = getseniormaterials(senior_material)
            ultimate_material = getultimatematerials(ultimate_material)
            skll_material = getskillmaterials(skll_material)

            Data = {
                "rolename" : besicinfo.get('role_name'),
                'roleimg' : besicinfo.get('role_img'),
                'roledescriptiontitle' : besicinfo.get('role_description_title'),
                'roledescription' : besicinfo.get('role_description'),
                'elementarytitle' : elementary_material.get('title'),
                'elementaryimg' : elementary_material.get('img'),
                'intermediatetitle' : intermediate_material.get('title'),
                'intermediateimg' : intermediate_material.get('img'),
                'seniortitle' : senior_material.get('title'),
                'seniorimg' : senior_material.get('img'),
                'ultimatetitle' : ultimate_material.get('title'),
                'ultimateimg' : ultimate_material.get('img'),
                'footagetitle' : ultimate_material.get('footagetitle'),
                'footageimg' : ultimate_material.get('footageimg'),
                'universaltitle' : ultimate_material.get('universaltitle'),
                'universalimg' : ultimate_material.get('universalimg'),
                'elementarymaterialtitle' : skll_material.get('elementarytitle'),
                'elementarymaterialimg' : skll_material.get('elementaryimg'),
                'intermediatematerialtitle' : skll_material.get('intermediatetitle'),
                'intermediatematerialimg' : skll_material.get('intermediateimg'),
                'seniormaterialtitle' : skll_material.get('seniortitle'),
                'seniormaterialimg' : skll_material.get('seniorimg'),
                'ultimatematerialtitle' : skll_material.get('ultimatetitle'),
                'ultimatematerialimg' : skll_material.get('ultimateimg'),
                'extratitle' : skll_material.get('extratitle'),
                'extraimg' : skll_material.get('extraimg'),
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
                    material_card = BytesIO(await page.screenshot(full_page=True))

                    # 关闭页面、上下文和浏览器
                    await page.close()
                    await context.close()
                    await browser.close()

        await material_cards.finish(MessageSegment.image(material_card))