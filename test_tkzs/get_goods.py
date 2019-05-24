import json
import os

import requests


def get_tkzs_key():
    home_path = os.getenv('HOME')
    conf_path = os.path.join(home_path, 'conf')
    key_conf = os.path.join(conf_path, 'tkzs_conf')
    with open(key_conf, 'r') as f:
        key = f.read()
    return key.strip()


# 所有商品
apkey = get_tkzs_key()

url = 'https://api.taokezhushou.com/api/v1/all'
param_url = {
    "app_key": apkey,
    "page": 2
}
res = requests.get(url, params=param_url)
res_json = res.text
res_dict = json.loads(res_json)
good_list = res_dict['data']
goods_id_list = []
coupon_id_list = []
for one in good_list:
    goods_id_list.append(one.get('goods_id'))
    coupon_id_list.append(one.get('coupon_id'))
