import os
import urllib

import requests
from bs4 import BeautifulSoup
import re

res = requests.get('https://www.pixiv.net/artworks/77023929', verify=False)

soup = BeautifulSoup(res.text, 'html.parser')

title = re.findall('illustTitle\":\".*?\"', soup.text)
print(title)
illustId = re.findall('illustId\":\".*?\"', soup.text)
print(illustId)

id = illustId[0].split(':')[1].split('"')[1]
print(id)
illtitle = title[0].split(":")[1].split('"')[1]
print(illtitle)
url = 'https://i.pximg.net/img-master/img/2019/09/29/17/19/34/77023929_p0_master1200.jpg'
url1 = 'https://i.pximg.net/user-profile/img/2018/05/20/17/31/42/14253653_b8099cb8852ed1670c70761b50159aad_50.jpg'
header = {
    #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'referer': 'https://www.pixiv.net/artworks/77023929',
    #'upgrade-insecure-requests': '1',
}

req = requests.get(url, headers=header)
print(req.content)
with open('./3.jpg', 'wb') as f:
    f.write(req.content)
f.close()
'''try:
    req = requests.get('https://i.pximg.net/img-master/img/2019/09/29/17/19/34/77023929_p0_master1200.jpg')
    print('获取文件成功...')
except:
    print('获取文件失败...')
with open('.', 'wb') as f:
    f.write(req.content)
f.close()'''
