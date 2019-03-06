import datetime

import chardet
import requests
from lxml import etree


# 得到翻译的网页
def get_translate_html(text):
    # text="哈哈哈，我最帅"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
    one_kind = "en"  # 中文转英文
    two_kind = "zh-CN"  # 英文转中文
    base_link = "http://translate.google.cn/m?hl=%s&sl=auto&q=%s"
    url = base_link % (one_kind, text)
    try:
        res = requests.get(url, headers=headers)
    except:
        print("一条记录不能解析%s" % (datetime.datetime.now()))
        return ""
    html_bytes = res.content
    code_style = chardet.detect(html_bytes).get("encoding")
    try:
        html_text = html_bytes.decode(code_style, "ignore")
    except:
        print(datetime.datetime.now())
        print("encoding is error")
        return ''
    return html_text


# 解析翻译的网页，获取最终的结果
def parse_res(res_html):
    compl_str = "/html/body/div[3]/text()"
    # 解析HTML文件
    try:
        tree = etree.HTML(res_html)
        res = tree.xpath(compl_str)
    except:
        print(datetime.datetime.now())
        print("can't parse html")
        return
    return res

# ##
def chinese_to_english(chinese_str):
    res = get_translate_html(chinese_str)
    eng_str = parse_res(res)
    if len(eng_str)>0:
        return eng_str[0]
    else:
        return None

