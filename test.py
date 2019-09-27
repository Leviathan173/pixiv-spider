
import requests
from bs4 import BeautifulSoup
res = requests.get("https://manhua.dmzj.com/siwangailisi")

b = BeautifulSoup(res.text, "html.parser")

img = b.select('#cover_pic')
print(img[0].get('src'))