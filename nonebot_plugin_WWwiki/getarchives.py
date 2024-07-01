from jinja2 import Template
import json
from bs4 import BeautifulSoup, NavigableString,Tag



def get_gift(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # 获取第一段文本
    first_p_text = soup.p.get_text(strip=True)
    # 获取图片的src属性
    img_src = soup.find('img')['src']
    hr_tag = soup.find('hr')
    content_after_hr = ''.join(str(s) for s in hr_tag.next_siblings if s != '\n')
    data = {
        'giftimg' : img_src,
        'gifttitle' : first_p_text,
        'giftcontent' : content_after_hr
    }
    return data




