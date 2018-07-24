import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn


# 定义中文分词器方法
def chinese_word_cut(mytext):
    return ' '.join(jieba.cut(mytext))


# 打印前几个词语
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


# 读取csv文件
df = pd.read_csv("datascience.csv", encoding='gb18030')

# print(df.head())
# print(df.shape)

# 获取文章分词后的字符串
df["content_cutted"] = df.content.apply(chinese_word_cut)

# i=1
# for one in df["content_cutted"]:
#     print(one)
#     i=i+1
#     print(i)

# 定义待分类的文章个数
n_features = 1000

# 定义tf分类器
tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df=0.5,
                                min_df=10)

# 获取分类器对象
tf = tf_vectorizer.fit_transform(df.content_cutted)

# 设置分类
n_topics = 100
# 进行算法运算
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50.0,
                                random_state=0)
# 开始进行运算
lda.fit(tf)

# 定义显示前多少位关键词
n_top_words = 20

# 获取关键字
tf_feature_names = tf_vectorizer.get_feature_names()
# 打印出关键字
print_top_words(lda, tf_feature_names, n_top_words)

#个性化打印输出
data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.show(data)
