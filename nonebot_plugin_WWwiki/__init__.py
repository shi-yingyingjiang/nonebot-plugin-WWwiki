from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .echo import echos
from .echocard import echo_cards
from .enemy import enemy_cards
from .help import help_img
from .recommendation import recommendation_cards
from .role_list import role_list
from .rolearchives import archive_cards
from .rolecard import character_cards
from .rolegift import gift_cards
from .rolematerial import material_cards
from .roleskll import skll_cards
from .roletale import tale_cards
from .weapon import weapon_cards

__plugin_meta__ = PluginMetadata(
    name='鸣潮wiki',
    description='查询鸣潮wiki相关内容',
    usage='鸣潮wiki帮助',
    type="application",
    homepage="https://github.com/shi-yingyingjiang/nonebot-plugin-WWwiki",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_htmlrender"),
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
            }
        ],
    },
)
