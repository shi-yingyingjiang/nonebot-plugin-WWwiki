from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command
from .getskll import get_recommendation
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import Get_link
from playwright.async_api import async_playwright
import os
from io import BytesIO
import httpx
import json
from jinja2 import Template







html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'recommendation', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'recommendation', 'out_page.html')



recommendation_cards = on_command('鸣潮角色配队推荐')

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



@recommendation_cards.handle()
async def recommendationcards(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_link(role_name,listdata)
    if role_id == None:
        await recommendation_cards.finish(f'没有找到角色,错误参数：' + role_name)
    else:
        async with httpx.AsyncClient() as client:
            roledata = {
                'id' : role_id
            }
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)

            info_data = get_basic_information(data)
            weapons_recommended_data = data.get('data').get('content').get('modules')[2].get('components')[0].get('tabs')[0].get('content')
            weapons_recommended = get_recommendation(weapons_recommended_data)
            echo_recommended_data = data.get('data').get('content').get('modules')[2].get('components')[0].get('tabs')[1].get('content')
            echo_recommended = get_recommendation(echo_recommended_data)
            team_recommended_data = data.get('data').get('content').get('modules')[2].get('components')[0].get('tabs')[2].get('content')
            team_recommended = get_recommendation(team_recommended_data)
            skll_recommended_data = data.get('data').get('content').get('modules')[2].get('components')[0].get('tabs')[3].get('content')
            skll_recommended = get_recommendation(skll_recommended_data)

            Data = {
                'roleimg': info_data.get('role_img'),
                'rolename': info_data.get('role_name'),
                'roledescription': info_data.get('role_description'),
                'roledescriptiontitle': info_data.get('role_description_title'),
                'weapons_recommended': weapons_recommended,
                'echo_recommended': echo_recommended,
                'team_recommended': team_recommended,
                'skll_recommended': skll_recommended
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
                    img = BytesIO(await page.screenshot(full_page=True))

                    # 关闭页面、上下文和浏览器
                    await page.close()
                    await context.close()
                    await browser.close()

            await recommendation_cards.finish(MessageSegment.image(img))