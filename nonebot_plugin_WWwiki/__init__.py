# coding=utf-8
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .echo import echos
from .echocard import echo_cards
from .enemy import enemy_cards,caseify
from .recommendation import recommendation_cards
from .role_list import role_list
from .rolearchives import archive_cards
from .rolecard import character_cards
from .rolegift import gift_cards
from .rolematerial import material_cards
from .roleskll import skll_cards
from .roletale import tale_cards
from .weapon import weapon_cards
from .activities import *
from .util import md_to_pic, UniMessage
from nonebot import on_command


__plugin_meta__ = PluginMetadata(
    name='鸣潮wiki',
    description='查询鸣潮wiki相关内容',
    usage='鸣潮wiki帮助',
    type="application",
    homepage="https://github.com/shi-yingyingjiang/nonebot-plugin-WWwiki",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_htmlrender", "nonebot_plugin_apscheduler", "nonebot-plugin-uninfo"),
    extra={
        'menu_data': [
            {
                'func': '查询角色信息',
                'trigger_method': '鸣潮角色查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮角色查询 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色技能',
                'trigger_method': '鸣潮技能查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮技能查询 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色共鸣链',
                'trigger_method': '鸣潮共鸣链查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮共鸣链查询 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色养成推荐',
                'trigger_method': '鸣潮角色配队推荐',
                'trigger_condition': ' ',
                'brief_des': '鸣潮角色配队推荐 安可',
                'detail_des': '无'
            },
            {
                'func': '查询珍贵之物',
                'trigger_method': '鸣潮珍贵之物',
                'trigger_condition': ' ',
                'brief_des': '鸣潮珍贵之物 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色档案',
                'trigger_method': '鸣潮角色档案',
                'trigger_condition': ' ',
                'brief_des': '鸣潮角色档案 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色故事',
                'trigger_method': '鸣潮角色故事',
                'trigger_condition': ' ',
                'brief_des': '鸣潮角色故事 安可',
                'detail_des': '无'
            },
            {
                'func': '查询角色突破材料',
                'trigger_method': '鸣潮突破材料',
                'trigger_condition': ' ',
                'brief_des': '鸣潮突破材料 安可',
                'detail_des': '无'
            },
            {
                'func': '查询武器信息',
                'trigger_method': '鸣潮武器查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮武器查询 时和岁稔',
                'detail_des': '无'
            },
            {
                'func': '查询声骸信息',
                'trigger_method': '鸣潮声骸查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮声骸查询 角',
                'detail_des': '无'
            },
            {
                'func': '查询敌人信息',
                'trigger_method': '鸣潮敌人查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮敌人查询 角',
                'detail_des': '无'
            },
            {
                'func': '查看卡池',
                'trigger_method': '鸣潮卡池列表',
                'trigger_condition': ' ',
                'brief_des': '无',
                'detail_des': '无'
            },
            {
                'func': '查看活动',
                'trigger_method': '鸣潮活动列表',
                'trigger_condition': ' ',
                'brief_des': '无',
                'detail_des': '无'
            },
            {
                'func': '自动推送即将开始或结束的活动',
                'trigger_method': '鸣潮活动提醒 --(开启/关闭)',
                'trigger_condition': '超级用户',
                'brief_des': '无',
                'detail_des': '无'
            },
            {
                'func': '查看角色列表',
                'trigger_method': '鸣潮角色列表',
                'trigger_condition': ' ',
                'brief_des': '无',
                'detail_des': '无'
            },
            {
                'func': '查看掉落物',
                'trigger_method': '鸣潮掉落物查询',
                'trigger_condition': ' ',
                'brief_des': '鸣潮掉落物 呓语声核',
                'detail_des': '无'
            },
        ],
    },
)

help = on_command("鸣潮wiki帮助")

@help.handle()
async def help_msg():
    ex = __plugin_meta__.extra["menu_data"]

    markdown_content = "# 鸣潮功能菜单\n\n"
    markdown_content += "| 功能名称 | 触发方法 | 触发条件 | 简要描述 | 详细描述 |\n"
    markdown_content += "| --- | --- | --- | --- | --- |\n"

    for item in ex:
        func = item['func']
        trigger_method = item['trigger_method']
        trigger_condition = item['trigger_condition']
        brief_des = item['brief_des']
        detail_des = item['detail_des']
        
        markdown_content += f"| {func} | {trigger_method} | {trigger_condition} | {brief_des} | {detail_des} |\n"

    img = await md_to_pic(markdown_content)

    await UniMessage.image(raw=img).finish()
