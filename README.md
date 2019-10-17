
## 简单易用！涩图爬虫！


## Attention!
如果你的网络可以直接访问`pixiv`，那么你可以去掉`util.py`中关闭ssl认证的相关代码

## 已知缺陷
动图无法正常获取，它不动的

多页只能抓第一张，可以通过`https://www.pixiv.net/ajax/illust/[index]/pages`来获取图片链接，但是最近有点忙，咕

R18标签下也有等级较高的没有过滤，例如[77178342](https://www.pixiv.net/artworks/77178342)

### Usage:
```
usage: main.py [-h] [-i INDEX] [-l LIMIT] [-r18 R18] [-ds DARKSIDE] [-n NUM]

涩图获取器 v0.1c by Leviathan173

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        需要爬取的页面的开始序号，默认77100000
  -l LIMIT, --limit LIMIT
                        最小被人喜欢的数值，只会爬取超过这个数值的涩图
  -r18 R18              是否只抓取涩图,1=是,2=否,3=我全都要
  -ds DARKSIDE, --darkside DARKSIDE
                        可怕的，不被大众接受的，那些你不会告诉别人的爱好，上帝不会原谅你的,0=关闭,1=开启
  -n NUM, --num NUM     要爬取多少张图片
```
### example
```
main.py -i 77180000 -l 100 -r18 no -n 10
```
