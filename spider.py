# encoding:utf-8
import argparse
import requests
import os
from bs4 import BeautifulSoup
from util import *


def spider_old(index, r18, limit, times):
    left_index = []
    while times > 0:
        print(f'进入下一页面，剩余任务{times}')
        indexs = get_allindex()
        if len(indexs) == 0:
            create_index(index)
        tags = ['\u5973\u306e\u5b50', '\u6c34\u7740', '\u306a\u306b\u3053\u308c\u304b\u308f\u3044\u3044']
        # tags_r18 = ['\u5973\u306e\u5b50', '\u6c34\u7740', '\u306a\u306b\u3053\u308c\u304b\u308f\u3044\u3044', 'R-18']

        # 获取网站数据
        # url = "https://www.pixiv.net/artworks/{}".format(index)
        url = "https://www.baidu.com"
        try:
            code = [404, 500, 503]
            res = requests.get(url)
            if res.status_code in code:
                print('页面不存在...')
                break
        except Exception as e:
            print('超时...')
            print('跳过，进入下一任务...')
            continue
        soup = BeautifulSoup(res.text, "html.parser")

        # 处理网站数据，获取喜欢的人数和tag
        iine = soup.select(".dROFhg > dd:nth-child(2)")
        print(iine.get_text)
        iineNum = int(iine.get_text())
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
    write_index(left_index)


def spider(index, r18, limit):
    """大致流程
    1、request获取pixiv.net/artwork/index的数据
    2、判断是否为要求的
    3、如果是，下载，返回index+1
    如果不是 index+1，返回1
    """
    RETRY_TIME = 5
    while True:
        # 获取
        url = f"https://www.pixiv.net/artworks/{index}"
        print(f'正在开始获取{url}的数据...')

        try:
            code = [404, 500, 503]
            requests.packages.urllib3.disable_warnings()
            res = requests.get(url, verify=False, timeout=(10, 30))
            if res.status_code in code:
                print('页面不存在...')
                index += 1
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
        except Exception as e:
            print(e)
            print('超时...')
            print('跳过，进入下一任务...')
            index += 1
            continue

        # 处理数据，获取标签和点赞数
        tags = get_tags(soup.text)
        iine = get_like_count(soup.text)
        if iine < limit:
            print('点赞数不足要求，跳过...')
            index += 1
            continue

        # 判断是否R18
        r18_flag = False
        tag_flag = False
        if R18 in tags:
            # TODO R18G内容筛选
            r18_flag = True

        # 判断是否存在用户tag
        for i in TAGLIB:
            if i in tags:
                tag_flag = True

        # 判断是否符合要求
        if r18:
            if r18_flag:
                if tag_flag:
                    print('发现符合，正在获取图片链接...')
                    img_url = get_img_url(soup.text)
                    for t in range(RETRY_TIME):
                        if dl(img_url, hash_name(get_ill_name(soup.text)),url) == 0:
                            print('下载完成...')
                            index += 1
                            write_index(index)
                            return index
                        else:
                            continue
                else:
                    print('存在R18但不存在所需标签，跳过...')
                    index += 1
                    continue
            else:
                print('不是R18，跳过...')
                index += 1
                continue
        else:
            if tag_flag:
                print('发现符合，正在获取图片链接...')
                img_url = get_img_url(soup.text)
                for t in range(RETRY_TIME):
                    if dl(img_url, hash_name(get_ill_name(soup.text)), url) == 0:
                        print('下载完成...')
                        index += 1
                        write_index(index)
                        return index
                    else:
                        print('下载出错，重试中...')
                        continue
            else:
                print('不存在所需标签，跳过...')
                index += 1
                continue
