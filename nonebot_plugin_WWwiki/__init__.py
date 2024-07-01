from .rolecard import character_cards
from .role_list import role_list
from .roleskll import skll_cards
from .ehcocard import ehco_card
from .recommendation import recommendation_cards
from .rolegift import gift_cards
from .rolematerial import material_cards
from .rolearchives import archive_cards
from .roletale import tale_cards
from nonebot.plugin import PluginMetadata
from nonebot import on_command


__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-WWwiki',
    description='查询鸣潮wiki相关内容',
    usage=' ',
    type="application",
    homepage="https://github.com/shi-yingyingjiang/nonebot-plugin-WWwiki",
    supported_adapters = {"nonebot.adapters.onebot.v11"},
    extra={
        'menu_data' : [
            {
                'func' : '查询角色信息',
                'trigger_method' : '鸣潮角色查询',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮角色查询 安可',
                'detail_des' : '无'
            },
            {
               'func' : '查询角色技能',
                'trigger_method' : '鸣潮技能查询',
               'trigger_condition' : ' ',
               'brief_des' : '鸣潮技能查询 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询角色共鸣链',
                'trigger_method' : '鸣潮共鸣链查询',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮共鸣链查询 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询角色养成推荐',
                'trigger_method' : '鸣潮角色配队推荐',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮角色配队推荐 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询珍贵之物',
                'trigger_method' : '鸣潮珍贵之物',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮珍贵之物 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询角色档案',
                'trigger_method' : '鸣潮角色档案',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮角色档案 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询角色故事',
                'trigger_method' : '鸣潮角色故事',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮角色故事 安可',
                'detail_des' : '无'
            },
            {
                'func' : '查询角色突破材料',
                'trigger_method' : '鸣潮突破材料',
                'trigger_condition' : ' ',
                'brief_des' : '鸣潮突破材料 安可',
                'detail_des' : '无'
            }
        ],
    }
)


