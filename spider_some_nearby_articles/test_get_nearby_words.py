import synonyms


# 对文本进行分词的方法
def fenci(s):
    res = synonyms.seg(s)
    if len(res) > 1:
        print("获取分词成功")
        return res[0]
    else:
        print("获取分词失败")
        return None


# 根据分词后的列表，获取他们的近义词，重新组合成一段话
def get_nearby_words(words_list):
    words = ""
    for one in words_list:
        nearby_words_tmp = synonyms.nearby(one)
        if len(nearby_words_tmp[0]) == 0:
            words = words + one
        else:
            words = words + nearby_words_tmp[0][1]
    return words


def get_new_words(str0):
    words_list = fenci(str0)
    words = get_nearby_words(words_list)
    return words
