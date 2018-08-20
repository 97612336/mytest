import json
import os
import qiniu.config
from qiniu import Auth, put_file, etag


def get_keys():
    home_path = os.getenv("HOME")
    conf_file_path = home_path + "/conf/qiniu_conf"
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    return conf_dict


res_dict = get_keys()
access_key = res_dict.get("ak")
secret_key = res_dict.get("sk")
q = Auth(access_key, secret_key)

bucket_name = "webfile"

key = "a.txt"

token = q.upload_token(bucket_name)
localfile = "./a.txt"

ret, info = put_file(token, key, localfile)

assert ret['key'] == key
assert ret['hash'] == etag(localfile)

print(info)
