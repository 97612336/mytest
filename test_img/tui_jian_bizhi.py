import datetime
import json
import urllib.request as ur


class Tui_jian_bizhi(object):
    def __init__(self):
        self.url=r'http://api.lovebizhi.com/windows_v3.php?a=everyday&spdy=1&device=&uuid=474e65d6bf02451296327143380e478a&mode=0&client_id=1004&device_id=74687137&model_id=106&size_id=0&channel_id=30001&screen_width=1366&screen_height=768&bizhi_width=1366&bizhi_height=768&version_code=33&language=zh-CN&mac=&date='

    def tui_jian(self):
        list_tuijian=[]
        time_now=datetime.datetime.now()
        time_current=time_now+datetime.timedelta(days=-30)
        str_time=time_current.strftime(r'%Y-%m-%d')
        url = self.url+str_time
        response=ur.urlopen(url)
        bytes_json=response.read()
        str_json=bytes_json.decode('utf-8')
        #得到json的字典数据
        dict_data=json.loads(str_json)
        #获取字典中的data的值,由集合组成
        list_data=dict_data['data']
        for one in list_data:
            #获取one下的'image'键的值,是一个字典:
            dict_image=one['image']
            small_photo=dict_image['small']
            normal_photo=dict_image['original']
            big_photo=dict_image['diy']
            list_one_image=[small_photo,normal_photo,big_photo]
            list_tuijian.append(list_one_image)
        return list_tuijian,str_time
