import urllib.request as ur

import time

start_time = time.time()
url_file = "http://p0yb78gzi.bkt.clouddn.com/a.txt"

resp = ur.urlopen(url_file)
res = resp.read()
print(res.decode('utf-8'))
end_time = time.time()
cost_time = end_time - start_time
print(cost_time)
