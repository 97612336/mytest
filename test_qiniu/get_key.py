import json
import os


def get_keys():
    home_path = os.getenv("HOME")
    conf_file_path = home_path + "/conf/qiniu_conf"
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    return conf_dict
