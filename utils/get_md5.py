import hashlib


def get_md5_str(id_string):
    md5 = hashlib.md5()
    md5.update(id_string.encode("utf-8"))
    picname = md5.hexdigest()
    return picname

