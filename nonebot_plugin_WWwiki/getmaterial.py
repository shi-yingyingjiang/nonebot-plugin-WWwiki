# coding=utf-8
from bs4 import BeautifulSoup

def role_breakthrough(html_content):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有的<img>标签
    img_tags = soup.find_all('img')

    # 提取第二个和第三个<img>标签及其对应的<a>标签的信息
    results = []
    for i in range(1, 3):  # 从索引1开始，提取第二个和第三个
        img = img_tags[i]
        # 查找img标签后面的<a>标签
        a = img.find_next('a')
        if a:
            src = img.get('src')
            text = a.get_text(strip=True)
            results.append((src, text))
        else:
            src = img.get('src')
            text = ''
            results.append((src, text))
    # img_tags = soup.find_all('img')
    # role_breakthrough_list = []
    # for i in range(1,3):
    #     img = img_tags[i]
    #     image_sources = img['src']
    #     # 获取img标签的父节点
    #     parent = img.parent
    #     # 获取父节点中的所有文本内容
    #     text_content = parent.get_text(strip=True)
    #     text_before_x = text_content.split('x')[0].strip()
    #     role_breakthrough_list.append((image_sources,text_before_x))

    # return role_breakthrough_list
    return results





skll_quantity_dict = {
    0:7,
    1:8,
    2:13,
    3:14,
    4:19,
    5:20,
    6:26,
    7:27,
    8:28,
}

def skill_breakthrough(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有的<img>标签
    img_tags = soup.find_all('img')

    # 提取src属性和对应的文字描述
    results = []
    for img in img_tags:
        src = img.get('src')
        # 查找img标签后面的文字描述
        a_tag = img.find_next('a')
        if a_tag:
            text = a_tag.get_text()
        else:
            text = ''
        results.append((src, text))

    skill_breakthrough_list = []

    for i in range(9):
        section = skll_quantity_dict[i]
        url, title = results[section]
        skill_breakthrough_list.append((url,title))

    return skill_breakthrough_list

