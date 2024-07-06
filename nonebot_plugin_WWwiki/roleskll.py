import json
from jinja2 import Template
from .basicinformation import get_basic_information
from .judgmentrolename import judgment_role_name
from .itemlink import Get_link
import os
from io import BytesIO
import httpx
from .getskll import extract_between_second_p_and_hr,extract_after_first_p
from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command



html_fpath = os.path.dirname(os.path.abspath(__file__))
html_spath = os.path.join(html_fpath, 'html_template', 'skllcard', 'template.html')
out_html_path = os.path.join(html_fpath, 'html_template', 'skllcard', 'out_page.html')



skll_cards = on_command('鸣潮技能查询')

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

@skll_cards.handle()
async def skllcard(args: Message = CommandArg()):
    role_name = judgment_role_name(args.extract_plain_text())
    role_id = await Get_link(role_name,listdata)
    if role_id ==None:
        await skll_cards.finish(f'没有找到角色,错误参数：' +  role_name)
    else:
        async with httpx.AsyncClient() as client:
            roledata = {
                'id' : role_id
            }
            roledataurl = 'https://api.kurobbs.com/wiki/core/catalogue/item/getEntryDetail'
            roledata_r = await client.post(roledataurl, data=roledata, headers=headers)
            data = json.loads(roledata_r.text)
            normal_attack_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[0].get('content')
            normal_attack = extract_between_second_p_and_hr(normal_attack_data)
            echo_skill_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[1].get('content')
            echo_skill = extract_between_second_p_and_hr(echo_skill_data)
            echo_loop_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[2].get('content')
            echo_loop = extract_between_second_p_and_hr(echo_loop_data)
            echo_liberation_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[3].get('content')
            echo_liberation = extract_between_second_p_and_hr(echo_liberation_data)
            modified_skill_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[4].get('content')
            modified_skill = extract_between_second_p_and_hr(modified_skill_data)
            prolonged_skill_data = data.get('data').get('content').get('modules')[1].get('components')[0].get('tabs')[5].get('content')
            prolonged_skill = extract_after_first_p(prolonged_skill_data)
            # echo_chain_data = data.get('data').get('content').get('modules')[1].get('components')[1].get('content')
            # echo_chain = get_html(echo_chain_data)

            info_data = get_basic_information(data)

            Data = {
                'normalattack': normal_attack.get('content'),
                'normalattacktitle': normal_attack.get('title'),
                'normalattackimg': normal_attack.get('img'),
                'echoskill': echo_skill.get('content'),
                'echoskilltitle': echo_skill.get('title'),
                'echoskillimg': echo_skill.get('img'),
                'echoloop': echo_loop.get('content'),
                'echoliberation': echo_liberation.get('content'),
                'modifiedskill': modified_skill.get('content'),
                'modifiedskilltitle': modified_skill.get('title'),
                'modifiedskillimg': modified_skill.get('img'),
                'prolongedskill': prolonged_skill.get('content'),
                'prolongedskilltitle': prolonged_skill.get('title'),
                'prolongedskillimg': prolonged_skill.get('img'),
                'roleimg' : info_data.get('role_img'),
                'rolename' : info_data.get('role_name'),
                'roledescription' : info_data.get('role_description'),
                'roledescriptiontitle' : info_data.get('role_description_title'),

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

            await skll_cards.finish(MessageSegment.image(skll_img))