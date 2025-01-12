# coding=utf-8
from jinja2 import Template
from bs4 import BeautifulSoup, NavigableString


def extract_between_second_p_and_hr(html):
    skll_data = {}
    soup = BeautifulSoup(html, 'html.parser')
    p_tags = soup.find_all('p')  # 找到所有<p>标签
    img_tag = soup.find('img')
    first_p_tag = soup.find('p')
    text_content = ' '.join(first_p_tag.stripped_strings)
    skll_data['title'] = text_content
    src_value = img_tag.get('src') if img_tag else None
    skll_data['img'] = src_value
    if len(p_tags) >= 2:  # 确保至少有两个<p>标签
        second_p = p_tags[1]  # 获取第二个<p>标签
        hr = second_p.find_next_sibling('hr')  # 从第二个<p>标签后查找<hr>
        if hr:
            # 获取从第二个<p>标签结束之后，直到<hr>标签之前的所有内容
            content = ''
            current = second_p
            while current and current != hr:
                if isinstance(current, NavigableString):
                    content += str(current)
                else:
                    content += str(current)
                current = current.next_sibling
            template = Template("{{ content }}")
            skll_content = template.render(content=content)
            skll_data['content'] = skll_content

    return skll_data


def extract_after_first_p(html):
    soup = BeautifulSoup(html, 'html.parser')
    skll_data = {}
    first_p = soup.find('p')
    img_tag = soup.find('img')
    first_p_tag = soup.find('p')
    text_content = ' '.join(first_p_tag.stripped_strings)
    skll_data['title'] = text_content
    src_value = img_tag.get('src') if img_tag else None
    skll_data['img'] = src_value
    # 找到第一个<p>标签
    if first_p:
        # 获取第一个<p>标签之后的全部内容（包括标签）
        content = str(first_p.next_sibling) + ''.join(str(s) for s in first_p.next_siblings)
        template = Template("{{ content }}")
        skll_content = template.render(content=content)
        skll_data['content'] = skll_content
        return skll_data


def get_recommendation(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a'):
        # 移除每个<a>标签的href属性
        del a_tag['href']
    table = str(soup.find('table'))

    return table
