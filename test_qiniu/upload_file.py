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


# 获取信息
res_dict = get_keys()
access_key = res_dict.get("ak")
secret_key = res_dict.get("sk")
# 利用ak和sk得到具体的用户
q = Auth(access_key, secret_key)

# 上传文件存储的仓库名
bucket_name = "webfile"
# 上传文件的用户名
key = "a.txt"

# 利用具体的用户得到具体的token
token = q.upload_token(bucket_name)

# 上传文件的地址
localfile = "./a.txt"

# 执行上传操作
ret, info = put_file(token, key, localfile)

#判断是否长传成功
assert ret['key'] == key
assert ret['hash'] == etag(localfile)


print(info)
