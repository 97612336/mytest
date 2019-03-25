import time
import datetime
import json
import os
from lxml import etree

import chardet
import pymysql
import requests

import synonyms


class Nearby_words:
    # 对文本进行分词的方法
    def fenci(self, s):
        res = synonyms.seg(s)
        if len(res) > 1:
            return res[0]
        else:
            return None

    # 根据分词后的列表，获取他们的近义词，重新组合成一段话
    def get_nearby_words(self, words_list):
        words = ""
        for one in words_list:
            nearby_words_tmp = synonyms.nearby(one)
            if len(nearby_words_tmp[0]) == 0:
                words = words + one
            else:
                words = words + nearby_words_tmp[0][3]
        return words

    def get_new_words(self, str0):
        words_list = self.fenci(str0)
        words = self.get_nearby_words(words_list)
        return words


# 随机从数据库中选择一张图片
def get_one_random_photo():
    # 获取数据库链接对象
    try:
        db = get_mysql_db()
    except Exception as e:
        print(e)
    cursor = db.cursor()
    sql_str = "select url from all_bizhi order by rand() limit 1;"
    cursor.execute(sql_str)
    res = cursor.fetchone()
    cursor.close()
    db.close()
    if len(res):
        return res[0]
    else:
        return None


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
def get_article_by_href(nw, one_href):
    article_html = get_html_text(one_href)
    # 获取文章标题
    article_title = html_parser(article_html, '//*[@id="article"]/div[1]/h2/text()')
    # 获取文章的内容
    article_content = html_parser(article_html,
                                  '//p/span[@class="bjh-p"]/text()')
    if article_title and article_content:
        tmp = {}
        tmp["title"] = nw.get_new_words(article_title[0])
        tmp["desc"] = nw.get_new_words(article_content[0])
        content_list = []
        # 遍历文章集合的元素，然后逐段翻译
        for one_content in article_content:
            tmp_content = {}
            new_one_content = nw.get_new_words(one_content)
            if new_one_content:
                new_one_content = new_one_content.replace("\"", "“").replace("\'", "“")
                tmp_content["type"] = 1
                tmp_content["text"] = new_one_content
                content_list.append(tmp_content)
                tmp_img = {}
                tmp_img["type"] = 0
                tmp_img["text"] = get_one_random_photo()
                content_list.append(tmp_img)
        tmp["content"] = content_list
        tmp["img"] = get_one_random_photo()
        return tmp
    else:
        return 0


# 根据解析到的数据保存到数据库中
def save_new_article_to_db(nw, cursor, article_data, one_word):
    title = article_data.get('title')
    info = article_data.get('desc')
    one_word = nw.get_new_words(one_word)
    content = pymysql.escape_string(str(article_data.get('content')))
    img = article_data.get("img")
    sql_str = 'insert into cn_articles (hot_word,title,info,content,img) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (
        one_word, title, info, content,img)
    try:
        cursor.execute(sql_str)
        db.commit()
        print("成功存入一条数据：%s" % datetime.datetime.now())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    nw = Nearby_words()
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
            # 根据一个搜索的关键词查询所有的百度快照url
            href_list = search_baijia_articles(one_word)
            for one_href in href_list:
                # 得到百度快照ＵＲＬ的内容
                article_data = get_article_by_href(nw, one_href)
                # 执行存入数据库的操作
                if article_data:
                    save_new_article_to_db(nw, cursor, article_data, one_word)
        cursor.close()
        db.close()
        # 休息十个小时
        print("运行完一次，休息20个小时")
        time.sleep(60 * 60 * 20)
