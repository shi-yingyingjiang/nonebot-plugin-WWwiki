import json
from jinja2 import Template
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import Get_link
import os
import httpx
from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command






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
html_spath = os.path.join(html_fpath, 'html_template', 'tale', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'tale', 'out_page.html')

tale_cards = on_command('鸣潮角色故事')


@tale_cards.handle()
async def _(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_link(role_name,listdata)
    if role_id ==None:
        await tale_cards.finish(f'没有找到角色,错误参数：' +  role_name)
    else:
        roledata = {
            'id' : role_id
        }
        async with httpx.AsyncClient() as client:
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            besicinfo = get_basic_information(data)
            content1 = data['data']['content']['modules'][3]['components'][2]['tabs'][0]['content']
            content2 = data['data']['content']['modules'][3]['components'][2]['tabs'][1]['content']
            content3 = data['data']['content']['modules'][3]['components'][2]['tabs'][2]['content']
            content4 = data['data']['content']['modules'][3]['components'][2]['tabs'][3]['content']
            content5 = data['data']['content']['modules'][3]['components'][2]['tabs'][4]['content']



            Data = {
                'rolename' : besicinfo.get('role_name'),
                'roleimg' : besicinfo.get('role_img'),
                'roledescriptiontitle' : besicinfo.get('role_description_title'),
                'roledescription' : besicinfo.get('role_description'),
                'content1' : content1,
                'content2' : content2,
                'content3' : content3,
                'content4' : content4,
                'content5' : content5
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
            archive_card = await page.screenshot(full_page=True,type='jpeg',quality=100)

            # 关闭页面、上下文和浏览器
            await page.close()
            await context.close()
            await browser.close()



    await tale_cards.finish(MessageSegment.image(archive_card))