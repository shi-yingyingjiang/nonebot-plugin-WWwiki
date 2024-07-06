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



weapon_cards = on_command('鸣潮武器查询')

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
    'catalogueId': '1106',
    'page': '1',
    'limit': '1000'
    }

html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'weapon', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'weapon', 'out_page.html')

@weapon_cards.handle()
async def get_weapon_data(args: Message = CommandArg()):
    name = args.extract_plain_text()
    weapon_id = await Get_link(name,listdata)
    if weapon_id == None:
        await weapon_cards.finish('没有找到武器,错误参数：' + name)
    else:
        weapondata = {
            'id' : weapon_id,
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
                'weaponimg' : img,
                'weaponname' : name,
                'attribute1' : attribute1,
                'attribute2' : attribute2,
                'description': description,
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
            aweapon_card = await page.screenshot(full_page=True,type='jpeg',quality=100)

            # 关闭页面、上下文和浏览器
            await page.close()
            await context.close()
            await browser.close()

    await weapon_cards.finish(MessageSegment.image(aweapon_card))