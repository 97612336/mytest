from random import Random

import requests
import time

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


# 生成随机的4位数字
def random_num(len_num):
    nums = ""
    chars = "0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(0, len_num):
        nums += chars[random.randint(0, length)]
    print(nums)
    return nums


# 从0开始往上加数字
def test_num_web():
    for i in range(16027,100000000000):
        name = str(i)
        print(name)
        res_num = can_use_web(name, ".com")
        time.sleep(1)
        if res_num != "0":
            print("+++++++++++++++++++++")
            print(name)
            print(res_num)
            print("+++++++++++++++++++++")
            write_name_to_file(name)
            

# 把数据写入文件
def write_name_to_file(name):
    with open("web_name3.txt", "a+") as f1:
        f1.write(name + "\n")


if __name__ == '__main__':
    # web_list = []
    # len_num = 4
    # while 1:
    #     name = random_username(len_num)
    #     # name = random_num(len_num)
    #     res_num = can_use_web(name, ".com")
    #     if res_num != "0":
    #         print("+++++++++++++++++++++")
    #         print(name)
    #         print(res_num)
    #         print("+++++++++++++++++++++")
    #         write_name_to_file(name)
    test_num_web()
