from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('../test_nltk/a.txt') as f1:
    text = f1.read()

word_cloud = WordCloud().generate(text)

plt.imshow(word_cloud,interpolation='bilinear')
plt.axis("off")
