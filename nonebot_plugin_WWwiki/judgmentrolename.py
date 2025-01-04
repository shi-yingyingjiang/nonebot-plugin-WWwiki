# coding=utf-8
from typing import Literal


class Drifter:
    def __init__(self, gender: Literal['男', '女'], attribute: str) -> None:
        self.gender = gender
        self.attribute = attribute

    @property
    def parameter(self) -> str:
        return f'漂泊者-{self.gender}-{self.attribute}'


def judgment_role_name(name: str):
    if '漂泊者' in name:
        enter = name
        attributes = ['衍射', '湮灭']

        # 提取性别和属性
        gender = '男' if '男' in enter else '女' if '女' in enter else None
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


if __name__ == '__main__':
    print(judgment_role_name('安可'))
