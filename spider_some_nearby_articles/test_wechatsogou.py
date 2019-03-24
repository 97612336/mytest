# -- coding: utf-8 --
import wechatsogou

words = "两颗天眼正式上岗"

ws_api = wechatsogou.WechatSogouAPI()

res = ws_api.search_article(words)

print(res)
