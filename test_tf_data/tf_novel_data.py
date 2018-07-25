import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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


# 获取series_data类型的数据
def get_series_data():
    # 读取csv文件,dataframe类型
    df = pd.read_csv("datascience.csv", encoding='gb18030')

    # 获取文章分词后的字符串,Series类型
    df["content_cutted"] = df.content.apply(chinese_word_cut)
    return df["content_cutted"]


# 得到tf分类器和tf分类器工具类
def get_tf_object(series_data, data_num):
    # 定义待分类的文章个数
    n_features = data_num

    # 定义tf分类器
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=10)

    # 把数据放入分类器中
    tf = tf_vectorizer.fit_transform(series_data)
    return tf, tf_vectorizer


# 训练数据,并分类
def fit_data(tf, kind_num):
    # 设置分类
    n_topics = kind_num
    # 进行算法运算
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.0,
                                    random_state=0)
    # 开始进行训模型
    lda.fit(tf)
    return lda


# 显示关键词信息
def show_topic_words(tf_vectorizer, lda):
    # 定义显示前多少位关键词
    n_top_words = 20

    # 获取关键字
    tf_feature_names = tf_vectorizer.get_feature_names()
    # 打印出关键字
    print_top_words(lda, tf_feature_names, n_top_words)


# 显示图表信息
def show_table(tf, tf_vectorizer, lda):
    # 个性化打印输出
    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)


def get_article_data():
    with open('../test_nltk/a.txt', 'r') as f1:
        all_text = f1.read()

    text_list_str = ' '.join(jieba.cut(all_text))
    text_list = text_list_str.split("当然")
    return pd.Series(text_list)


def main():
    series_data = get_article_data()
    tf, tf_tool = get_tf_object(series_data, 228)
    lda = fit_data(tf, 10)
    # 显示关键词信息
    show_topic_words(tf_tool, lda)
    # 显示表格
    show_table(tf, tf_tool, lda)


main()
