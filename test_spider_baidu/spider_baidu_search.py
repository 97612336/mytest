import requests

url = "http://cache.baiducontent.com/c?m=9d78d513d9961cb8599dca2d5140c321590a8f397a91925468d5e0558e34051c1271e3cc76634658c4c50b3b56e9540cbdac66256b1427c39bca8b4dc0e8d26e74d979636d4ad107418847eed6432fc420975cedaa&p=aa769a47818511a053ebcb655540&newp=82769a47839f18ff57e6922c1b5d92695d0fc20e36d1c44324b9d71fd325001c1b69e7bf25211502d5c37e6c03aa485becfb3678341766dada9fca458ae7c47d73d1&user=baidu&fm=sc&query=goland&qid=f948d83f0003ecb1&p1=1"



response = requests.get(url)
response.encoding="gb2312"
print(response.text)
