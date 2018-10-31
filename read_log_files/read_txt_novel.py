import pickle
import time

import chardet

path = "/home/wangkun/Downloads/神控天下.txt"


def get_str(some_bytes):
    code_style = chardet.detect(some_bytes).get("encoding")
    res_txt = some_bytes.decode(code_style, "ignore")
    return res_txt


def get_text_from_read():
    with open(path, "rb") as f1:
        lines = f1.read()
        res_txt = get_str(lines)

    res_list = res_txt.splitlines()
    print(type(res_list))
    print(len(res_list))
    print("*****************************")
    return res_list


def pickle_list_to_file(res_list):
    with open("txt_list_pickle", 'wb') as f2:
        pickle.dump(res_list, f2)


def get_pickle_list():
    with open("txt_list_pickle", 'rb') as f2:
        res_list = pickle.load(f2)
    print(type(res_list))
    print(len(res_list))
    return res_list


if __name__ == '__main__':
    start_time = time.time()
    # res_list = get_text_from_read()
    res_list = get_pickle_list()
    pickle_list_to_file(res_list)
    end_time = time.time()
    i = 0
    for one in res_list:
        if str(one).startswith("第"):
            print(one)
            print(i)
            print(res_list[i])
            print("============================")
        i = i + 1
    print("++++++++++++++++++++++++++++++")
    print(res_list[len(res_list) - 10])
    print(end_time - start_time)
