from urllib.parse import urlencode
from urllib.request import Request, urlopen

title = "这是标题"
message = "this is message"
sound = "this is sound"
vibration = "this is vibration"
icon = "this is icon"
iconcolor = 'this is iconcolor'
device = 'this is device'
urltitle = 'this is urltitle'
private_key = "<privatekey>"
url = 'https://www.pushsafer.com/api'  # Set destination URL here
post_fields = {  # Set POST fields here
    "t": title,
    "m": message,
    "s": sound,
    "v": vibration,
    "i": icon,
    "c": iconcolor,
    "d": device,
    "u": url,
    "ut": urltitle,
    "k": private_key
}

request = Request(url, urlencode(post_fields).encode())
json = urlopen(request).read().decode()
print(json)
