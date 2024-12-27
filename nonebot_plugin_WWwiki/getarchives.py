# coding=utf-8
from bs4 import BeautifulSoup


def get_gift(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # 获取第一段文本
    if not soup.p:
        raise ValueError(soup)
    first_p_text = soup.p.get_text(strip=True)
    # 获取图片的src属性
    img_src = soup.find('img')['src']
    hr_tag = soup.find('hr')
    if not hr_tag:
        raise ValueError(soup)
    content_after_hr = ''.join(str(s) for s in hr_tag.next_siblings if s != '\n')
    data = {
        'giftimg': img_src,
        'gifttitle': first_p_text,
        'giftcontent': content_after_hr
    }
    return data
