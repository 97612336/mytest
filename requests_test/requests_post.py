from random import Random

import requests


# 判断网址是否存在
def can_use_web(name, suffix):
    url = "https://hk.wopop.com/ajax/domainQuery.ashx"

    data = {
        "oper": "queryDomainStatus",
        "mnytpe": 2,
        "u_prc": 1,
        "domainName": name,
        "domainSuffix": suffix
    }

    res = requests.post(url=url, data=data)
    res_list = str(res.text).split("|")
    return res_list[-1]


# 随机生成4到20位的字符串
def random_username(len_num):
    username = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(0, len_num):
        username += chars[random.randint(0, length)]
    print(username)
    return username


# 把数据写入文件
def write_name_to_file(name):
    with open("web_name2.txt", "a+") as f1:
        f1.write(name + "\n")


if __name__ == '__main__':
    web_list = []
    len_num = 4
    while 1:
        name = random_username(len_num)
        res_num = can_use_web(name, ".com")
        if res_num != "0":
            print("+++++++++++++++++++++")
            print(name)
            print(res_num)
            print("+++++++++++++++++++++")
            write_name_to_file(name)
