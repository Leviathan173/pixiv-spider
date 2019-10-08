# pixiv-spider
## 简单易用！涩图爬虫！
### Usage:
```
usage: main.py [-h] [-i INDEX] [-l LIMIT] [-r18 R18] [-n NUM]

涩图获取器 v0.1c by Leviathan173

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        需要爬取的页面的开始序号，默认77100000
  -l LIMIT, --limit LIMIT
                        最小被人喜欢的数值，只会爬取超过这个数值的涩图
  -r18 R18              是否只抓取涩图，yes or no
  -n NUM, --num NUM     要爬取多少张图片
```
### example
```
main.py -i 77180000 -l 100 -r18 no -n 10
```