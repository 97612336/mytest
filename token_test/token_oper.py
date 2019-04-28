import hashlib
import time


def get_md5_str(id_string):
    md5 = hashlib.md5()
    md5.update(id_string.encode("utf-8"))
    picname = md5.hexdigest()
    return picname


def create_token(time_num, token_tag, username):
    all_str = str(time_num) + token_tag + username
    token = get_md5_str(all_str)
    return token


def check_token(time_num, username, token):
    all_str = str(time_num) + "this_is_token" + username
    token_tmp = get_md5_str(all_str)
    print(token_tmp)
    if token == token_tmp:
        return True
    else:
        return False


if __name__ == '__main__':
    time_num = time.time()
    token_tag = "this_is_token"
    token = create_token(time_num=time_num, token_tag=token_tag, username="wangkun")
    print(token)
    res = check_token(time_num=time_num, username='wangkun', token=token)
    print(res)
