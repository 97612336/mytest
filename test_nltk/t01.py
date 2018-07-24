import nltk
import jieba

# 读取文件
res = open('./a.txt').read()

# 对文件内容进行分词
words_list = jieba.lcut(res)
print(type(words_list))

# 获取文本对象
text = nltk.text.Text(words_list)

# 统计这样的词出现的次数,并显示文章内容
# text.concordance("哈哈")

# 获取该词在文本中出现的位置
# text.common_contexts(["神"])

