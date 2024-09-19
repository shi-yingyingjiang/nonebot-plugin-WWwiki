import asyncio
from typing import Dict, List
import httpx
from datetime import datetime, timedelta
import json
from nonebot import on_command,logger
from nonebot.permission import SUPERUSER
from .util import UniMessage, get_template, template_to_pic,get_activities,scheduler
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

    ra_name = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['description']

    roleimglist = []
    for i in range(0,4):
        roleimgs = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['imgs'][i]['img']
        roleimglist.append(roleimgs)

    role_dict["contentUrl"] = roleimglist
    role_dict["title"] = ra_name



    weapon_dict = {}

    wa_name = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][0]['description']

    weaponimglist = []
    for i in range(0,4):
        weaponimgs = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][0]['imgs'][i]['img']
        weaponimglist.append(weaponimgs)

    weapon_dict["contentUrl"] = weaponimglist
    weapon_dict["title"] = wa_name


    ac_list = []
    ac_list.append(role_dict)
    ac_list.append(weapon_dict)


    rw_dict['activities'] = ac_list


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


#卡池
def role_data(data):
    role = data['ac'][0]['activities'][0]
    weapon = data['ac'][0]['activities'][1]
    time = data['ac'][0]['dateRange']
    # end_time = datetime.strptime(time[1], "%Y-%m-%d %H:%M")

    Data = {
        "time1" : time[0],
        "time2" : time[1],
        "timeperiod" : compare_time_ranges(time),
        "rolename" : role['title'],
        "fivestarsimg" : role['contentUrl'][0],
        "fourstarsimg1" : role['contentUrl'][1],
        "fourstarsimg2" : role['contentUrl'][2],
        "fourstarsimg3" : role['contentUrl'][3],
        "weaponname" : weapon['title'],
        "fiveswi" : weapon['contentUrl'][0],
        "fourswi1" : weapon['contentUrl'][1],
        "fourswi2" : weapon['contentUrl'][2],
        "fourswi3" : weapon['contentUrl'][3]
    }


    return Data



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

card_pools = on_command('鸣潮卡池')

card_pool_spath = get_template("card_pool")
activity_spath = get_template("activity")
data_spath = get_activities()




@card_pools.handle()
async def cardpools():
    old_data = await get_data()

    Data = role_data(old_data)


    img = await template_to_pic(
        card_pool_spath.parent.as_posix(),
        card_pool_spath.name,
        Data,
        
    )

    await UniMessage.image(raw=img).finish()



activities = on_command('鸣潮活动列表')


@activities.handle()
async def activity():
    old_data = await get_data()


    Data = {
        "div" : ac(old_data['ac'])
    }


    img = await template_to_pic(
        activity_spath.parent.as_posix(),
        activity_spath.name,
        Data,
        
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

            img = await template_to_pic(
                timing_activity.parent.as_posix(),
                timing_activity.name,
                Data,
                
            )

            for group_id in CONFIG['opened_groups']:

                target = Target(group_id)
                logger.info(f'成功推送活动')
                await UniMessage.image(raw=img,).send(target=target)


        else:
            return



alc = Alconna("鸣潮活动提醒", Args["group_id?", int], Option("-o|--开启"), Option("-c|--关闭"))

reminder = on_alconna(alc,permission=SUPERUSER)
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
    
    

        