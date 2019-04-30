# 获取配置文件列表
import pickle


def get_info_list():
    with open('urls_list.pickle', "rb") as f:
        res_list = pickle.load(f)
    return res_list


res_list = get_info_list()
res_list.pop()
res_list.pop(0)
for one_kind in res_list:
    print(one_kind.get('kind_name'))
    kind_content = one_kind.get('kind_content')
    for i in kind_content:
        print(i.get('name'))
        print(i.get('img'))
        print(i.get('url'))
        print('\n')
    print('====================')
