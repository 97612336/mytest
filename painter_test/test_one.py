import json
import os

import imgkit
import requests
from pyecharts import Radar

api1 = 'http://47.94.133.29/backstage_detail/warning_describe/?id=300266201708031&end_date=2018-09-03 '
api2 = 'http://47.94.133.29/backstage_detail/warning_describe/?id=300266201708031&end_date=2018-09-03 '


def get_api_dict(url):
    json_one = requests.get(url).text
    radar_dict_str = json.loads(json_one)['risk_radar']
    radar_dict = json.loads(radar_dict_str)
    return radar_dict


name_dict = {
    "market_wave": "行情异动",
    "big_trans": "大宗交易",
    "holder_reduce": "股东减持",
    "equities_pledge": "股权质押",
    "market_news": "市场消息",
    "investor_wave": "投资者异动",
    "report_abnormal": "财报异常",
    "good_anno": "利好公告"
}

# 创建雷达HTML
dict_one = get_api_dict(api1)
radar = Radar("预警雷达", is_animation=False)
value_list = [[]]
c_schema = []
for key, value in dict_one.items():
    tmp = {}
    name = name_dict[key]
    tmp['name'] = name
    tmp['max'] = 1
    tmp['min'] = -1
    c_schema.append(tmp)
    value_list[0].append(value)
print(value_list)
print(c_schema)
radar.config(c_schema=c_schema)
radar.add('图形一', value_list, legend_text_size=20, area_color='red', area_opacity=0.5)
radar.render('radar.html')

# 生成radar.png图片
imgkit.from_file('radar.html', 'radar.jpg')
