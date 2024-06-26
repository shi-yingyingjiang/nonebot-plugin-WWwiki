import json
from jinja2 import Template
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .rolelink import Get_role_link
import os
from io import BytesIO
import httpx
from .getarchives import get_gift
from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command




html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'gift', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'gift', 'out_page.html')



gift_cards = on_command('鸣潮珍贵之物')

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests' : '1',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Ch-Ua' : '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Wiki_type' : '9'

}


@gift_cards.handle()
async def giftcard(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_role_link(role_name)
    if role_id == None:
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
            gift_one_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[0].get('content')
            gift_one = get_gift(gift_one_data)
            gift_two_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[1].get('content')
            gift_two = get_gift(gift_two_data)
            gift_three_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[2].get('content')
            gift_three = get_gift(gift_three_data)
            gift_four_data = data.get('data').get('content').get('modules')[3].get('components')[1].get('tabs')[3].get('content')
            gift_four = get_gift(gift_four_data)

            Data = {
                'roleimg': info_data.get('role_img'),
                'rolename': info_data.get('role_name'),
                'roledescription': info_data.get('role_description'),
                'roledescriptiontitle': info_data.get('role_description_title'),
                'giftimgo' : gift_one.get('giftimg'),
                'gifttitleo' : gift_one.get('gifttitle'),
                'giftcontento' : gift_one.get('giftcontent'),
                'giftimg2' : gift_two.get('giftimg'),
                'gifttitle2' : gift_two.get('gifttitle'),
                'giftcontent2' : gift_two.get('giftcontent'),
                'giftimg3' : gift_three.get('giftimg'),
                'gifttitle3' : gift_three.get('gifttitle'),
                'giftcontent3' : gift_three.get('giftcontent'),
                'giftimg4' : gift_four.get('giftimg'),
                'gifttitle4' : gift_four.get('gifttitle'),
                'giftcontent4' : gift_four.get('giftcontent'),
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
            skll_img = BytesIO(await page.screenshot(full_page=True))

            # 关闭页面、上下文和浏览器
            await page.close()
            await context.close()
            await browser.close()

    await gift_cards.finish(MessageSegment.image(skll_img))