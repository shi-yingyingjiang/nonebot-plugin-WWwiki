import httpx
import json
import os
from .itemlink import Get_link
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot import on_command
from jinja2 import Template
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup




echos = on_command('鸣潮声骸查询',aliases={'声骸查询'})

getentrydetail = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'

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
    'catalogueId': '1107',
    'page': '1',
    'limit': '1000'
    }

html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'echo', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'echo', 'out_page.html')


@echos.handle()
async def _(args: Message = CommandArg()):
    name = args.extract_plain_text()
    echo_id = await Get_link(name,listdata)
    if echo_id == None:
        await echos.finish('没有找到该声骸')
    else:
        echodata = {
            'id' : echo_id
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(getentrydetail,data=echodata,headers=headers)
            data = json.loads(res.text)
            img_content = data['data']['content']['modules'][0]['components'][0]['content']
            soup = BeautifulSoup(img_content,'html.parser')
            img = soup.find('img')
            name = data['data']['name']
            src = img['src']
            info = data['data']['content']['modules'][0]['components'][1]['content']
            skll = data['data']['content']['modules'][0]['components'][2]['tabs'][0]['content']

            Data = {
                'name' : name,
                'img' : src,
                'info' : info,
                'skll' : skll
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
            echo_card = await page.screenshot(full_page=True,type='jpeg',quality=100)

            # 关闭页面、上下文和浏览器
            await page.close()
            await context.close()
            await browser.close()

    await echos.finish(MessageSegment.image(echo_card))