
import requests  #Python向服务器发起网络请求

def getHtml(url):
    req=requests.get(url=url)
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace') #如果设置为replace，则会用?取代非法字符；
    return encode_content

