# coding=utf-8
from typing import Literal
import random


class Drifter:
    def __init__(self, gender: str, attribute: str) -> None:
        self.gender = gender
        self.attribute = attribute

    @property
    def parameter(self) -> str:
        return f'漂泊者-{self.gender}-{self.attribute}'


def judgment_role_name(name: str):
    namelist={
        '光主': '漂泊者衍射',
        '暗主': '漂泊者湮灭',
        '风主': '漂泊者气动',
        '电主': '漂泊者导电',
        '雷主': '漂泊者导电',
        '冰主': '漂泊者冷凝',
        '火主': '漂泊者热熔',
        '漂泊者': '漂泊者'
    }
    if any(elem in name for elem in namelist):
        enter = name
        for key,value in namelist.items():
            enter = enter.replace(key,value)
        attributes = ['衍射', '湮灭','气动','导电','冷凝','热熔']
        thegender= random.choice(['男', '女'])

        # 提取性别和属性
        gender = '男' if '男' in enter else '女' if '女' in enter else thegender
        if gender is not None:
            attribute_in_enter = [attr for attr in attributes if attr in enter]
            if attribute_in_enter:
                # 使用提取的性别和属性创建 Drifter 实例
                drifter = Drifter(gender, attribute_in_enter[0])
                role_name = drifter.parameter
            else:
                role_name = f"没有找到匹配的属性。"
        else:
            role_name = f"没有找到漂泊者的性别。"
    else:
        role_name = name

    return role_name


def yituliu_role_name(name: str):
    namelist={
        '光主': '衍射漂泊者',
        '暗主': '湮灭漂泊者',
        '风主': '气动漂泊者',
        '电主': '导电漂泊者',
        '雷主': '导电漂泊者',
        '冰主': '冷凝漂泊者',
        '火主': '热熔漂泊者',
        '漂泊者': '漂泊者'
    }
    if any(elem in name for elem in namelist):
        enter = name
        for key,value in namelist.items():
            enter = enter.replace(key,value)
        attributes = ['衍射', '湮灭','气动','导电','冷凝','热熔']

       

        attribute_in_enter = [attr for attr in attributes if attr in enter]
        if attribute_in_enter:
            role_name = f"{attribute_in_enter[0]}漂泊者"
        else:
            role_name = name  # 无匹配属性时返回原名或处理后的名称
    else:
        role_name = name

    return role_name