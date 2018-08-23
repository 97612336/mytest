import urllib.request as ur
import json

class Search_tsz_photos(object):

    #获取所有URL的壁纸
    def get_all_photo(self,str_search):
        #总的图片列表
        list_all_page_photo=[]
        # 将文字进行utf-8格式转码
        str_search = ur.quote(str_search)
        start_num=0
        while 1:
            url = r'http://wallpaper.apc.360.cn/index.php?c=WallPaper&a=search&start=' + str(start_num) + '&count=100&kw=' + str(str_search)
            start_num=start_num+100
            #一页的图片
            list_one_page_photo=self.search_one_page_photo(url)
            #所有页的图片
            list_all_page_photo=list_all_page_photo+list_one_page_photo
            #一页数据不够100,就终止循环
            if len(list_one_page_photo)!=100 or len(list_all_page_photo)>500:
                break
        return list_all_page_photo

    #获取一页的搜索关键字的所有图片
    def get_only_one_page(self,str_search,page):
        # 将文字进行utf-8格式转码
        str_search = ur.quote(str_search)
        start_num = 50*int(page)
        url = r'http://wallpaper.apc.360.cn/index.php?c=WallPaper&a=search&start=' + str(
            start_num) + '&count=50&kw=' + str(str_search)
        list_one_page_photo=self.search_one_page_photo(url)
        return list_one_page_photo


    #根据一个url获取所有的壁纸
    def search_one_page_photo(sef,url):
        # url = r'http://wallpaper.apc.360.cn/index.php?c=WallPaper&a=search&start='+str(start_num)+'&count=100&kw='+str(str_search)
        response = ur.urlopen(url)
        bytes_json = response.read()
        str_json = bytes_json.decode('utf-8')
        obj_json = json.loads(str_json)
        # 获取字典中的data的值,由集合组成
        list_data = obj_json['data']
        # 'img_1366_768' 最后大1049088        # img_1280_1024  第二大
        # img_1600_900   最大        # img_1440_900   第三大
        # url        # utag        # url_mid        # url_thumb        # url_mobile
        # 一页的总的图片列表
        list_one_page_photo=[]
        #遍历每一张图片字典
        for dict_one_photo in list_data:
        #     #一个图片的字典
            one_photo={}
        #     #遍历一张图片的所有key
            list_keys=dict_one_photo.keys()
        #     #得到一张中等图片的url
            if 'img_1366_768' in list_keys:
                one_photo['medium_photo']=dict_one_photo['img_1366_768']
            else:
                one_photo['medium_photo'] = dict_one_photo['url']
        #     #得到一张大图的url
            if 'img_1600_900' in list_keys:
                one_photo['larger_photo'] = dict_one_photo['img_1600_900']
            elif 'img_1280_1024' in list_keys:
                one_photo['larger_photo'] = dict_one_photo['img_1280_1024']
            elif 'img_1440_900' in list_keys:
                one_photo['larger_photo']=dict_one_photo['img_1440_900']
            else:
                one_photo['larger_photo']=dict_one_photo['url']
            #获取一张小图的URL
            if 'url_mid' in list_keys:
                one_photo['little_photo']=dict_one_photo['url_mid']
            elif 'url_thumb' in list_keys:
                one_photo['little_photo'] = dict_one_photo['url_thumb']
            else:
                one_photo['little_photo'] =''
        #     #获取一张图片的tag标签
            if 'utag' in list_keys:
                one_photo['words']=dict_one_photo['utag']
            else:
                one_photo['words'] = ''
        #     #把这个图片字典加到这一页的图片集合当中
            list_one_page_photo.append(one_photo)
        return list_one_page_photo


# s=Search_tsz_photos()
# list_photo=s.get_all_photo('熊猫')
# print(len(list_photo))
# for one in list_photo:
#     print(one)
# list1=s.get_only_one_page('美女',2)
# print(len(list1))
# print(list1)