import json
import os

import requests
from requests.cookies import RequestsCookieJar

session = requests.session()


# api配置信息
def get_info():
    home_path = os.getenv('HOME')
    conf_path = os.path.join(home_path, 'conf')
    key_conf = os.path.join(conf_path, 'tkzs_conf')
    with open(key_conf, 'r') as f:
        res_text = f.read()
    info_dict = json.loads(res_text)
    return info_dict


# 模拟登录
######################
login_url = 'http://www.taokezhushou.com/login'
login_data = {
    "mobile": "18610211913",
    "password": get_info().get('password')
}
login_res = session.post(login_url, data=login_data)
with open('b.html', 'w') as f:
    f.write(login_res.text)
######################

# is_login_url = 'http://www.taokezhushou.com/checklogin'
#
# is_login_res = session.get(is_login_url)

# c = RequestsCookieJar()
# c.set('cookie-name', 'cookie-value')
# session.cookies.update(c)
# print(session.cookies.get_dict())
cookies_dict = session.cookies.get_dict()
# print(cookies_dict)
######################

url = 'http://www.taokezhushou.com/zhuanlian'

data = {
    "goods_id": "583057046377",
    "coupon_id": "78ec59c96a0f464dbdbda8f4340a83e0",
    'text': '【买1送1】湖南特产剁辣椒酱',
    'pid': 'mm_53822622_17578204_63648225',
    'resp': 'td'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36",
}

res = requests.post(url=url, data=data, cookies=cookies_dict, headers=headers)

res_dict = json.loads(res.text)
print(res_dict)
