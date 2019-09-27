# encoding:utf-8
import argparse
import requests
import os
from bs4 import BeautifulSoup
from dl_img import *
from find_index import *


def spider(index, r18, limit, times):
    left_index = []
    while times > 0:
        print('进入下一页面，剩余任务{}'.format(times))
        indexs = get_allindex()
        if len(indexs) == 0:
            create_index(index)
        tags = ['\u5973\u306e\u5b50', '\u6c34\u7740', '\u306a\u306b\u3053\u308c\u304b\u308f\u3044\u3044']
        # tags_r18 = ['\u5973\u306e\u5b50', '\u6c34\u7740', '\u306a\u306b\u3053\u308c\u304b\u308f\u3044\u3044', 'R-18']

        # 获取网站数据
        url = "https://www.pixiv.net/artworks/{}".format(index)
        try:
            res = requests.get(url)
        except Exception as e:
            print('超时...')
            print('跳过，进入下一任务...')
            continue
        soup = BeautifulSoup(res.text, "html.parser")

        # 处理网站数据，获取喜欢的人数和tag
        iine = soup.select(".sc-LzNMr > li:nth-child(1) > dl:nth-child(1) > dd:nth-child(2)")
        iineNum = int(iine.get_text)
        print('iine={}'.format(iineNum))
        tag = soup.select("._1LEXQ_3 > li > span > a")
        print(tag)
        r18Flag = False
        is_wanted = False
        for i in range(len(tag)):
            # tag筛选条件
            if tag[i] == 'R-18':
                r18Flag = True
            if tag[i] in tags:
                is_wanted = True

        # 判断是否是想要的
        if r18 is True and r18Flag is True:
            # 获取涩图下载链接并保存
            dl_url = soup.select('.sc-LzNtV').get('src')
            indexs.remove(index)
            dl(dl_url, index)
            times -= 1
        elif r18 is False and r18Flag is False and is_wanted is True:
            dl_url = soup.select('.sc-LzNtV').get('src')
            indexs.remove(index)
            dl(dl_url, index)
            times -= 1
        else:
            indexs.remove(index)
        left_index = indexs.copy()
    write_left(left_index)
