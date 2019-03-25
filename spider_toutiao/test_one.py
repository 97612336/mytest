import requests
from lxml import etree
import chardet
import datetime


# 获取URL的网页HTML
def get_html_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
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


def html_parser(html_text, compl_str):
    # 解析HTML文件
    try:
        tree = etree.HTML(html_text)
        res = tree.xpath(compl_str)
    except Exception as e:
        print(datetime.datetime.now())
        print(e)
        print("can't parse html")
        return
    return res


url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=" + "两颗天眼正式上岗"

html_text = get_html_text(url)
print(html_text)
