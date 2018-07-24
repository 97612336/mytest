import nltk
import jieba

# 读取文件
res = open('./a.txt').read()

# 对文件内容进行分词
words_list = jieba.lcut(res)
# print(words_list)
freq = nltk.FreqDist(words_list)

# 根据分词获取他们的词语出现的次数
# for key, value in freq.items():
#     print(key)
#     print(type(key))
#     print(value)
#     print(type(value))

# 分词之后的字典
text_dict = freq.items()

sorted_text = sorted(text_dict,key=lambda k :k[1])

print(sorted_text)

freq.plot(30)

