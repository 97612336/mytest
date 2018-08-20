import urllib.request as ur

url_file = "http://p0yb78gzi.bkt.clouddn.com/a.txt"

resp = ur.urlopen(url_file)
res = resp.read()
print(res.decode('utf-8'))
