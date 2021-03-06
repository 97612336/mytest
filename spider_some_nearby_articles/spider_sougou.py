import time
import datetime
import json
import os
from lxml import etree

import chardet
import pymysql
import requests


###翻译模块
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
    if eng_str:
        return eng_str[0]
    else:
        return None


# 获取sql db
def get_mysql_db():
    home_path = os.getenv("HOME")
    conf_file_path = home_path + "/conf/sqlconf"
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    conn = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                           user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                           db="bigbiy_web", charset='utf8mb4')
    return conn


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


baidu_url = "http://www.baidu.com/baidu?wd="
baidu_fengyun_url = "http://top.baidu.com/"


# 得到热搜的关键词
def get_fengyun_words():
    words_list = []
    fengyun_res = get_html_text(baidu_fengyun_url)
    # 得到实时热点关键词
    now_hot_words = html_parser(fengyun_res, '//*[@id="hot-list"]/li/a[@class="list-title"]/text()')
    if now_hot_words:
        words_list = words_list + now_hot_words
    # 得到七日关注热词
    seven_day_words = html_parser(fengyun_res,
                                  '//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/ul/li/a[@class="list-title"]/text()')
    words_list = words_list + seven_day_words
    # 得到今日上榜热词
    new_hot_words_tmp = html_parser(fengyun_res, '//*[@id="flip-list"]/div[1]/div/div/a/text()')
    new_hot_words = []
    for one_word in new_hot_words_tmp:
        new_one_word = str(one_word).strip()
        new_hot_words.append(new_one_word)
    words_list = words_list + new_hot_words
    #     得到民生热点词
    man_life_words = html_parser(fengyun_res,
                                 '//*[@id="box-cont"]/div[4]/div[2]/div/div[2]/div[1]/ul/li/div[1]/a[@class="list-title"]/text()')
    words_list = words_list + man_life_words
    #     得到热门搜索
    hot_search_words = html_parser(fengyun_res,
                                   '//*[@id="box-cont"]/div[8]/div[2]/div/div[2]/div[1]/ul/li/div[1]/a[@class="list-title"]/text()')
    words_list = words_list + hot_search_words
    words_set = set(words_list)
    return words_set


# 搜索热词，得到热词网页
def search_hot_words(one_hot_word):
    new_url = baidu_url + one_hot_word
    html_text = get_html_text(new_url)
    # 获取百度快照url
    href_list = html_parser(html_text, '//div[@class="result c-container "]/div[@class="f13"]/a[@class="m"]/@href')
    return href_list


# 根据一个快照链接，得到具体的网页内容
def get_content_by_one_href(one_href):
    html_text = get_html_text(one_href)
    head_str = '<div style="position:relative">'
    body_str_tmp = html_text.split('<div style="position:relative">')[-1]
    body_str = body_str_tmp.split('</body>')[0]
    new_html = head_str + body_str
    return new_html


# 执行存入数据库的操作
def save_to_db(one_word, html_str):
    db = get_mysql_db()
    cursor = db.cursor()
    new_html = pymysql.escape_string(html_str)
    sql_str = "insert into articles (html,hot_word) VALUES(\'%s\',\'%s\');" % (new_html, one_word)
    cursor.execute(sql_str)
    db.commit()
    print("成功存入一条数据：%s" % datetime.datetime.now())
    cursor.close()
    db.close()


# 删除一周前的内容
def del_week_age_articles():
    db = get_mysql_db()
    cursor = db.cursor()
    # 获取当前时间
    now_time = datetime.datetime.now() - datetime.timedelta(days=7)
    now_time_str = str(now_time)
    sql_str = "delete from articles where save_time<'%s';" % (now_time_str)
    res = cursor.execute(sql_str)
    print("删除了%s行数据" % res)
    db.commit()
    cursor.close()
    db.close()


###########################
# 根据热搜词搜索百家号文章链接
def search_baijia_articles(one_word):
    new_url = baidu_url + one_word + "%20百家号"
    html_str = get_html_text(new_url)
    href_res = html_parser(html_str, '//div[@class="result c-container "]/h3[@class="t"]/a/@href')
    return href_res


# 根据一个链接，查询链接内文章所有的内容
def get_article_by_href(one_href):
    article_html = get_html_text(one_href)
    # 获取文章标题
    article_title = html_parser(article_html, '//*[@id="article"]/div[1]/h2/text()')
    # 获取文章的内容
    article_content = html_parser(article_html,
                                  '//p/span[@class="bjh-p"]/text()')
    # 获取文章的图片
    article_imgs = html_parser(article_html, '//div[@class="img-container"]/img/@src')
    if article_title and article_content:
        tmp = {}
        tmp["title"] = chinese_to_english(article_title[0])
        tmp["desc"] = chinese_to_english(article_content[0])
        content_list = []
        # 遍历文章集合的元素，然后逐段翻译
        for one_content in article_content:
            new_one_content = chinese_to_english(one_content)
            if new_one_content:
                new_one_content = new_one_content.replace("\"", "“").replace("\'", "“")
                content_list.append(new_one_content)
        tmp["content"] = content_list
        tmp['imgs'] = article_imgs
        return tmp
    else:
        return 0


# 根据解析到的数据保存到数据库中
def save_new_article_to_db(cursor, article_data, one_word):
    title = article_data.get('title')
    info = article_data.get('desc')
    one_word = chinese_to_english(one_word)
    content = pymysql.escape_string(str(article_data.get('content')))
    imgs = pymysql.escape_string(str(article_data.get('imgs')))
    sql_str = 'insert into articles (hot_word,title,info,content,imgs) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (
        one_word, title, info, content, imgs)
    try:
        cursor.execute(sql_str)
        db.commit()
        print("成功存入一条数据：%s" % datetime.datetime.now())
    except Exception as e:
        print(e)


################################
################################
############ V2 ################
################################
################################
################################


# 根据热词去搜索搜狗的微信文章
def get_weixin_pages(one_word):
    new_href_list = []
    url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query=" + one_word
    html_text = get_html_text(url)
    href_list = html_parser(html_text, '//div[@class="txt-box"]/h3/a/@href')
    print(len(href_list))
    for one_href in href_list:
        if str(one_href).startswith("https://weixin.sogou.com"):
            new_href_list.append(one_href)
        else:
            new_href_list.append("https://weixin.sogou.com" + one_href)
    for one_href in new_href_list:
        with open("a.txt", "a+") as f:
            f.write(one_href + "\n")


if __name__ == '__main__':
    while 1:
        # 获取数据库链接对象
        try:
            db = get_mysql_db()
        except Exception as e:
            print(e)
            break
        cursor = db.cursor()
        # 得到所有搜索的热词
        hot_set = get_fengyun_words()
        print("共得到%s个关键词" % len(hot_set))
        # 遍历每个热词，然后搜索每个热词，得到html网页里所有百度的链接
        for one_word in hot_set:
            one_word = "两颗天眼正式上岗"
            get_weixin_pages(one_word)
            # 根据得到的热词去搜索搜狗微信

            break
        cursor.close()
        db.close()
        break
        # # 休息十个小时
        # print("运行完一次，休息20个小时")
        # time.sleep(60 * 60 * 20)
