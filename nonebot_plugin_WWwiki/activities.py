# coding=utf-8
import asyncio
from typing import Dict, List
import httpx
from datetime import datetime, timedelta
import json
from nonebot import on_command,logger
from nonebot.permission import SUPERUSER
from jinja2 import Template
from nonebot_plugin_uninfo.permission import ADMIN
from .pil_draw.draw import draw_main
from .pil_draw.tools import save_image
from .util import UniMessage, get_template,get_activities,scheduler
from nonebot_plugin_alconna import on_alconna,Target,Match
from nonebot_plugin_alconna.uniseg import MsgTarget
from arclet.alconna import Alconna, Option,Args
from aiofiles import open as aio_open
from .config import group_data
lock = asyncio.Lock()






 
url = 'https://api.kurobbs.com/wiki/core/homepage/getPage'

data = {

}


headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests' : '1',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Ch-Ua' : '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Wiki_type' : '9'

}



if group_data.exists():
    with open(group_data, "r", encoding="utf8") as f:
        CONFIG: Dict[str, List] = json.load(f)
else:
    CONFIG: Dict[str, List] = {"opened_groups": []}
    with open(group_data, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)


#处理数据
async def get_data():
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, headers=headers)

    dw = resp.json()

    activities_dict = {}

    rw_dict = {}
    rwtime = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['countDown']['dateRange']
    rw_dict['dateRange'] = rwtime


    role_dict = {}
    role_pool = []
    role_pool_tab = dw['data']['contentJson']['sideModules'][0]['content']['tabs']
    for ii in range(0,len(role_pool_tab)):


        ra_name = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][ii]['name']

        roleimglist = []
        for i in range(0,4):
            roleimgs = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][ii]['imgs'][i]['img']
            roleimglist.append(roleimgs)

        role_dict["contentUrl"] = roleimglist
        role_dict["title"] = ra_name
        role_pool.append(role_dict)





    weapon_dict = {}
    weapon_pool = []
    weapom_pool_tab = dw['data']['contentJson']['sideModules'][1]['content']['tabs']
    for ii in range(0,len(weapom_pool_tab)):

        wa_name = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][ii]['name']

        weaponimglist = []
        for i in range(0,4):
            weaponimgs = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][0]['imgs'][i]['img']
            weaponimglist.append(weaponimgs)

        weapon_dict["contentUrl"] = weaponimglist
        weapon_dict["title"] = wa_name
        weapon_pool.append(weapon_dict)
    


    ac_dict = {}
    ac_dict["role"] = role_pool
    ac_dict["weapon"] = weapon_pool


    rw_dict['activities'] = ac_dict


    activities = dw['data']['contentJson']['sideModules'][2]['content']

    activities_with_countdown = [activity for activity in activities if 'countDown' in activity]




    result = []

    result.append(rw_dict)
    seen_date_ranges = set()

    for activity in activities_with_countdown:
        date_range_str = activity.get("countDown", {}).get("dateRange")
        if date_range_str:
            # 直接使用字符串形式的日期范围作为键
            key = tuple(date_range_str)
        else:
            key = None

        if key not in seen_date_ranges:
            seen_date_ranges.add(key)
            result.append({"dateRange": key, "activities": []})

        index = next(i for i, item in enumerate(result) if item["dateRange"] == key)
        result[index]["activities"].append({
            "contentUrl": activity["contentUrl"],
            "title": activity["title"]
        })




    activities_dict['ac'] = result
    return activities_dict




def is_current_time_in_range(time_list):
    # 定义日期时间格式
    date_format = "%Y-%m-%d %H:%M"

    start_str = time_list[0]
    # end_str = time_list[1] + timedelta(days=1)

    end_datetime = datetime.strptime(time_list[1], date_format) + timedelta(days=1)

# 将结果转换回字符串
    end_str = end_datetime.strftime(date_format)
    
    # 将字符串转换为datetime对象
    start_time = datetime.strptime(start_str, date_format).date()
    end_time = datetime.strptime(end_str, date_format).date()
    
    # 获取当前时间
    current_time = datetime.now().date()
    
    # 判断当前时间是否在范围内
    if start_time <= current_time <= end_time:
        return True
    else:
        return False
    

# 2判断是否存在符合条件的活动
def check_activities(data):
    is_start_previous_day = False
    is_end_previous_day = False

    current_date = datetime.now().date()

    for item in data:
        start_date_str, end_date_str = item["dateRange"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M").date()

        # 判断开始前一天
        if start_date - timedelta(days=1) == current_date:
            is_start_previous_day = True

        # 判断结束前一天
        if end_date - timedelta(days=1) == current_date:
            is_end_previous_day = True

    # 如果是开始前一天或结束前一天则返回True，否则返回False
    return is_start_previous_day or is_end_previous_day


#3输出符合条件的活动
def get_activities_before_and_after_today(data):

    ac_dict = {}


    # 当前时间
    current_date = datetime.now().date()  

    # 分类列表
    start_previous_day = []
    end_previous_day = []

    # 遍历数据
    for item in data:
        start_date_str, end_date_str = item["dateRange"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M").date()

        # 判断开始前一天
        if start_date - timedelta(days=1) == current_date:
            start_previous_day.extend(item["activities"])

        # 判断结束前一天
        if end_date - timedelta(days=1) == current_date:
            end_previous_day.extend(item["activities"])

    # 输出结果
    before = []
    for activity in start_previous_day:
        before.append(activity)

    ac_dict["before"] = before

    after = []
    for activity in end_previous_day:
        after.append(activity)

    ac_dict["after"] = after

    return ac_dict


# 定义一个函数来计算时间差
def calculate_time_difference(end_time):
    if end_time < current_time:
        return "已结束"
    
    delta = end_time - current_time
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    
    return f"剩余：{days}天 {hours}小时 {minutes}分钟"

def compare_time_ranges(time_ranges):
    # 获取当前时间
    current_time = datetime.now()
    current_time_date = current_time.date()
    
    # 解析输入的时间范围
    start_time = datetime.strptime(time_ranges[0], "%Y-%m-%d %H:%M")
    start_time_date = start_time.date()
    end_time = datetime.strptime(time_ranges[1], "%Y-%m-%d %H:%M")
    end_time_date = end_time.date()

    # 比较并输出结果
    if current_time_date < start_time_date:
        return "未开始"
    elif current_time_date > end_time_date:
        return "已结束"
    else:
        # 计算与结束时间的差
        delta = end_time - current_time
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        
        return f"{days}天 {hours}小时 {minutes}分钟"






current_time = datetime.now()

# 定义日期格式
date_format = "%Y-%m-%d %H:%M"

# 定义HTML模板
template = '''
<div class="ot">
    <div class="img">
        <img src="{img}" class="aimg">
    </div>
    <div class="atitle">
        <h1 class="at">{title}</h1>
        <h1 class="time">{start_time} - {end_time}</h1>
        <h1 class="tp">{time_diff}</h1>
    </div>
</div>
'''




#活动列表
def ac(data):
    html_content = ""
    for item in data[1:]:  # 从第二个字典开始
        date_range = item["dateRange"]
        activities = item["activities"]
        
        # 转换日期字符串为datetime对象
        start_time, end_time = [datetime.strptime(date, date_format) for date in date_range]
        
        
        # 计算时间差
        time_diff = compare_time_ranges(date_range)
        
        for activity in activities:
            if isinstance(activity["contentUrl"], list):
                img_url = activity["contentUrl"][0]  # 使用第一个图片URL
            else:
                img_url = activity["contentUrl"]
            title = activity["title"]
            
            html_content += template.format(img=img_url, title=title, start_time=start_time, end_time=end_time, time_diff=time_diff)


    return html_content


def get_end(data):
    before_template = """
    <div class="t">
    <div class="ot">
    <div class="img">
        <img src="{img}" class="aimg"> </div>
    <div class="atitle">
        <h1 class="at">{title}</h1></div></div></div>
    """
    before_htmls = """
    <div class="oo">
        <h1 class="title">以下活动将于明天开始</h1></div>
    """
    for item in data['before']:
        if isinstance(item["contentUrl"], list):
            img_url = item["contentUrl"][0]  # 使用第一个图片URL
        else:
            img_url = item["contentUrl"]
        before_htmls += before_template.format(img=img_url, title=item['title'])
        
    # output_dict['before'] = before_htmls

    # Process 'after'
    after_template = """
    <div class="t">
    <div class="ot">
    <div class="img">
        <img src="{img}" class="aimg"> </div>
    <div class="atitle">
        <h1 class="at">{title}</h1></div></div></div>
    """
    after_htmls = """
    <div class="oo">
        <h1 class="title">以下活动将于明天结束</h1></div>
    """
    

    for item in data['after']:
        if isinstance(item["contentUrl"], list):
            img_url = item["contentUrl"][0]  # 使用第一个图片URL
        else:
            img_url = item["contentUrl"]
        after_htmls += after_template.format(img=img_url, title=item['title'])

        

    return after_htmls + before_htmls

activity_spath = get_template("activity")
data_spath = get_activities()






async def get_html_content(data):
    html_template = '''
    <div class="block">
    <div class="img">
        <img src="{img}" class="roleimg imgborder"></div>
    <div class="titlebody">
        <h1 class="title">{name}</h1>
        <h1 class="timeinterval">{timeinterval}</h1>
        <h1 class="remainingtime">{remainingtime}</h1>
        <div class="h-full  bg-gray-200 rounded-full role="progressbar" aria-valuemin="0" aria-valuemax="100">
        <div class="h-full  rounded-full {color}" style="{progress}"></div>
        </div></div></div>'''

    html_content = ""
    activities = data['data']['contentJson']['sideModules'][2]['content']
    activities_with_countdown = [activity for activity in activities if 'countDown' in activity]
    result = []
    seen_date_ranges = set()

    for activity in activities_with_countdown:
        date_range_str = activity.get("countDown", {}).get("dateRange")
        if date_range_str:
            # 直接使用字符串形式的日期范围作为键
            key = tuple(date_range_str)
        else:
            key = None

        if key not in seen_date_ranges:
            seen_date_ranges.add(key)
            result.append({"dateRange": key, "activities": []})

        index = next(i for i, item in enumerate(result) if item["dateRange"] == key)
        result[index]["activities"].append({
            "contentUrl": activity["contentUrl"],
            "title": activity["title"]
        })
    
    for item in result:
        date = item["dateRange"]
        activities = item["activities"]
        current_date = datetime.now()

        start_date = datetime.strptime(date[0], "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(date[1], "%Y-%m-%d %H:%M")

        # 检查年份是否相同
        if start_date.year == end_date.year:
            # 年份相同，去除年份
            formatted_date_string = f"{start_date.strftime('%m.%d %H:%M')}-{end_date.strftime('%m.%d %H:%M')}"
        else:
            # 年份不同，保留完整日期
            formatted_date_string = f"{start_date.strftime('%Y.%m.%d %H:%M')}-{end_date.strftime('%Y.%m.%d %H:%M')}"



        # 计算目标日期区间的总天数
        total_days = (end_date - start_date).days + 1

        # 计算当前日期到目标日期区间的剩余天数
        if current_date < start_date:
            remaining_days = total_days
        elif current_date > end_date:
            remaining_days = 0
        else:
            remaining_days = (end_date - current_date).days + 1

        # 计算剩余时间占比
        if total_days == 0:
            remaining_percentage = 0
        else:
            remaining_percentage = (remaining_days / total_days) * 100

        if current_date  < start_date:
            Time_remaining = f"未开始"
        elif current_date  > end_date:
            Time_remaining = f"已结束"
        else:
            # 计算与结束时间的差
            delta = end_date - current_date 
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds // 60) % 60
            Time_remaining = f"{days}天{hours}小时{minutes}分钟"

        if remaining_days == 0 or current_date < start_date:
            color_class = "bg-gray-200"
        elif remaining_percentage <= 33.33:
            color_class = "bg-red-300"
        elif remaining_percentage <= 66.67:
            color_class = "bg-yellow-300"
        else:
            color_class = "bg-green-300"

        for i in range(0,len(activities)):
            img_url = activities[i]['contentUrl']
            title = activities[i]['title']
            html_content += html_template.format(img=img_url,name=title,timeinterval=formatted_date_string,remainingtime=Time_remaining,color=color_class,progress=f"width: {remaining_percentage}%")

    return html_content


async def pool(data):
    roles =  data['data']['contentJson']['sideModules'][0]['content']['tabs']
    weapons =  data['data']['contentJson']['sideModules'][1]['content']['tabs']
    date_list = data['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['countDown']['dateRange']
    roles_data = []
    weapons_data = []
    for tab in roles:
        tab_info = {
            "name": tab["name"],
            "imgs": [img["img"] for img in tab["imgs"]]
        }
        roles_data.append(tab_info)

    for tab in weapons:
        tab_info = {
            "name": tab["name"],
            "imgs": [img["img"] for img in tab["imgs"]]
        }
        weapons_data.append(tab_info)


    # 获取当前日期
    current_date = datetime.now()

    # 定义目标日期区间
    start_date = datetime.strptime(date_list[0], "%Y-%m-%d %H:%M") # 目标区间的开始日期
    end_date = datetime.strptime(date_list[1], "%Y-%m-%d %H:%M")  # 目标区间的结束日期
    if start_date.year == end_date.year:
            # 年份相同，去除年份
        formatted_date_string = f"{start_date.strftime('%m.%d %H:%M')}-{end_date.strftime('%m.%d %H:%M')}"
    else:
        # 年份不同，保留完整日期
        formatted_date_string = f"{start_date.strftime('%Y.%m.%d %H:%M')}-{end_date.strftime('%Y.%m.%d %H:%M')}"

    # 计算目标日期区间的总天数
    total_days = (end_date - start_date).days + 1

    # 计算当前日期到目标日期区间的剩余天数
    if current_date < start_date:
        remaining_days = total_days
    elif current_date > end_date:
        remaining_days = 0
    else:
        remaining_days = (end_date - current_date).days + 1

    # 计算剩余时间占比
    if total_days == 0:
        remaining_percentage = 0
    else:
        remaining_percentage = (remaining_days / total_days) * 100

    if remaining_days == 0 or current_date < start_date:
        color_class = "bg-gray-200"
    elif remaining_percentage <= 33.33:
        color_class = "bg-red-300"
    elif remaining_percentage <= 66.67:
        color_class = "bg-yellow-300"
    else:
        color_class = "bg-green-300"



    # 计算时间差
    time_difference = end_date - current_date

    # 提取天数、秒数
    days = time_difference.days
    seconds = time_difference.seconds

    # 计算小时数和分钟数
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    Time_remaining = f'{days}天{hours}小时{minutes}分钟'

    html_template = '''
    <div class="rolepool">
        <div class="pool">
        <div class="role">
        <div class="fivestar">
            <img src="{fiveimg}" class="fiveimg"></div>
        <div class="fourstar">
            <img src="{fourimg1}" class="fourimg">
            <img src="{fourimg2}" class="fourimg">
            <img src="{fourimg3}" class="fourimg"></div></div>
        <div class="weapon">
            <img src="{weapon1}" class="wimg">
            <img src="{weapon2}" class="wimg">
            <img src="{weapon3}" class="wimg">
            <img src="{weapon4}" class="wimg"></div> </div>
        <div class="progress">
            <h1 class="title">{rolename}-{weaponname}</h1>
            <h1 class="timeinterval">{timeinterval}</h1>
            <h1 class="remainingtime">{remainingtime}</h1> 
            <div class="h-full  bg-gray-200 rounded-full role="progressbar" aria-valuemin="0" aria-valuemax="100">
                <div class="h-full  rounded-full {color}" style="{progress}"></div></div></div></div>
    '''
    html_content = ''
    for i in range(len(roles_data)):
        fiveimg = roles_data[i]['imgs'][0]
        fourimg1 = roles_data[i]['imgs'][1]
        fourimg2 = roles_data[i]['imgs'][2]
        fourimg3 = roles_data[i]['imgs'][3]
        weapon1 = weapons_data[i]['imgs'][0]
        weapon2 = weapons_data[i]['imgs'][1]
        weapon3 = weapons_data[i]['imgs'][2]
        weapon4 = weapons_data[i]['imgs'][3]
        rolename = roles_data[i]['name']
        weaponname = weapons_data[i]['name']

        html_content += html_template.format(fiveimg=fiveimg, fourimg1=fourimg1, fourimg2=fourimg2, fourimg3=fourimg3, weapon1=weapon1, weapon2=weapon2, weapon3=weapon3, weapon4=weapon4, rolename=rolename, weaponname=weaponname, timeinterval=formatted_date_string, remainingtime=Time_remaining, color=color_class,progress=f"width: {remaining_percentage}%")

    
    

    



    return html_content

activities = on_command('鸣潮活动')


@activities.handle()
async def activity():
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, headers=headers)
    acdata = resp.json()
    pool_content = await pool(acdata)
    activity_content = await get_html_content(acdata)
    


    Data = {
        "pool_content" : pool_content,
        "activity_content" : activity_content
    }

    img = await draw_main(
        Data,
        activity_spath.name,
        activity_spath.parent.as_posix(),
    )

    await UniMessage.image(raw=img).finish()


timing_activity = get_template("timing")


@scheduler.scheduled_job('cron',hour='18',jitter=600)
async def scheduled_tasks():
        old_data = await get_data()


        if check_activities(old_data['ac']) is True:
            ac_dict_data = get_activities_before_and_after_today(old_data['ac'])
            ac_dica = get_end(ac_dict_data)

            Data = {
                "div" : ac_dica
            }

            img = await draw_main(
                Data,
                timing_activity.name,
                timing_activity.parent.as_posix(),
            )

            for group_id in CONFIG['opened_groups']:

                target = Target(group_id)
                logger.info(f'成功推送活动')
                await UniMessage.image(raw=img,).send(target=target)


        else:
            return



alc = Alconna("鸣潮活动提醒", Args["group_id?", int], Option("-o|--开启"), Option("-c|--关闭"))

reminder = on_alconna(alc,permission=SUPERUSER|ADMIN())
@reminder.assign("开启")
async def open(target: MsgTarget):
    if not target.private:
        groupid = target.id
        if groupid in CONFIG["opened_groups"]:
            await reminder.finish("该群已开启活动提醒")
        else:
            CONFIG["opened_groups"].append(groupid)
    async with lock:
        async with aio_open(group_data, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
    await reminder.finish("开启成功")


@reminder.assign("关闭")
async def close(target: MsgTarget): 
    if not target.private:
        groupid = target.id
        if groupid in CONFIG["opened_groups"]:
            CONFIG["opened_groups"].remove(groupid)
            async with lock:
                async with aio_open(group_data, 'w', encoding='utf-8') as f:
                        await f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
            await reminder.finish("关闭成功")
        else:
            await reminder.finish("该群未开启活动提醒")
    
    

        