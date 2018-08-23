import re
import urllib.request as ur
import os

# url = r'http://588ku.com/sucai/0-default-0-0-xiongmao-1/'
import chardet
from xpinyin import Pinyin


class Get_qianku_photo(object):

    #得到指定页数的所有图片列表
    def get_all_photo_url(self,str0,num1):
        print('进入方法了')
        list0=[]
        p = Pinyin()
        str1 = p.get_pinyin(str0, '')
        for i in range(1,num1+1):
            url='http://588ku.com/sucai/0-default-0-0-'+str1+'-'+str(i)+'/'
            r=self.get_one_page_photo_url(url)
            list0=list0+r
        print('解析完成了')
        return list0

    #获取指定页数的一页的所有图片和链接
    def get_only_one_page(self,str0,page):
        p=Pinyin()
        str1=p.get_pinyin(str0,'')
        url = 'http://588ku.com/sucai/0-default-0-0-' + str1 + '-' + str(page) + '/'
        print('搜索的url: ',url)
        result=self.get_one_page_photo_url(url)
        return result

    #这个方法是被上个方法调用的
    def get_one_page_photo_url(self,url):
        list_img_and_url = []
        headers = {
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With" : "XMLHttpRequest",
		    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
		    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"

        }
        request = ur.Request(url, headers=headers)
        response = ur.urlopen(request)
        html = response.read()
        resu = chardet.detect(html)
        code0 = resu['encoding']
        html = html.decode(code0, 'ignore').replace(u'\xa9', u'')
        print(html)
        r = re.findall(r'http://bpic\.588ku\.com/element_pic.+?\.html', html)
        if r:
            r.pop()
        for one in r:
            new_list = one.split('"')
            list_one_url_and_img = [new_list[0], new_list[len(new_list) - 1]]
            list_img_and_url.append(list_one_url_and_img)
        return list_img_and_url

    # 大图页中的图片链接（此方法是为了获得当前页面的大图）
    def get_one_big_photo(self, url):
        headers = {
          # "Accept" : "application/json, text/javascript, */*; q=0.01",
           # "X-Requested-With" : "XMLHttpRequest",
	 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
		   # "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
		}
        request = ur.Request(url, headers=headers)
        response = ur.urlopen(request)
        html = response.read()
        resu = chardet.detect(html)
        code0 = resu['encoding']
        html = html.decode(code0, 'ignore')
        # print(html)
        r = re.findall(r'http://bpic\.588ku\.com/+element_origin_min_pic/.*.jpg', html)
        # print(r)
        if len(r) > 1:
            return r[0]
        return r[0]

    #封装所有的方法，返回大图和小图的二维列表
    def get_little_and_big_photo(self,str):
        list_all_littleimg_and_bigimg=[]
        list_littleimg_and_url=self.get_all_photo_url(str,10)
        print('开始解析大图和小图')
        for one in list_littleimg_and_url:
            list_one_littleing_and_bigimg=[]
            list_one_littleing_and_bigimg.append(one[0])
            one_big_photo=self.get_one_big_photo(one[1])
            list_one_littleing_and_bigimg.append(one_big_photo)
            list_all_littleimg_and_bigimg.append(list_one_littleing_and_bigimg)
        print('方法快要结束了')
        return list_all_littleimg_and_bigimg



# glp=Get_qianku_photo()
# list1=glp.get_all_photo_url('熊猫',1)
# print(len(list1))
# for i in list1:
#     print(i)
# url=r'http://588ku.com/sucai/0-default-0-0-xiongmao-0-6/'
# res=glp.get_one_page_photo_url(url)
# print(len(res))
# url=r'http://588ku.com/sucai/7139312.html'
# list=glp.get_one_big_photo(url)
# print(list)
# list_all_little_and_big=glp.get_little_and_big_photo('熊猫')
# print(len(list_all_little_and_big))
# list1=glp.get_only_one_page('xiongmao',3)
# print(len(list1))
# print(list1)