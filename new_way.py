import re

import requests
from bs4 import BeautifulSoup
from util import *

res = requests.get('https://www.pixiv.net/artworks/77023929', verify=False)

soup = BeautifulSoup(res.text, 'html.parser')

print(f'iine={get_like_count(soup.text)}')
print(f'tag={get_tags(soup.text)}')
print(f'img_url={get_img_url(soup.text)}')

dl(get_img_url(soup.text), hash_name(get_ill_name(soup.text)))