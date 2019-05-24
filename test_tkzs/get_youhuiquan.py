import requests
from requests.cookies import RequestsCookieJar

session = requests.session()
# 模拟登录
######################
login_url = 'http://www.taokezhushou.com/login'
login_data = {
    "mobile": "18610211913",
    "password": ""
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
######################

url = 'http://www.taokezhushou.com/zhuanlian'

data = {
    "goods_id": "590206784802",
    "coupon_id": "2c81a3603d34430aa83d15e8e4a61758",
    'text': '女式拖鞋沙滩防滑人字拖鞋女夏季外穿夹脚',
    'pid': 'mm_53822622_17578204_63648225',
    'resp': 'td'
}

res = requests.post(url=url, data=data, cookies=cookies_dict)
print(res.text)
