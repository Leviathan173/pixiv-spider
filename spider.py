# encoding:utf-8
import argparse
import requests
import os
from bs4 import BeautifulSoup
from util import *


def spider(index, r18, limit, ds):
    """大致流程
    1、request获取pixiv.net/artwork/index的数据
    2、判断是否为要求的
    3、如果是，下载，index+1,返回index
    如果不是 index+1，重试
    """

    while True:
        # 获取
        url = f"https://www.pixiv.net/artworks/{index}"
        print(f'正在开始获取{url}的数据...')

        res = get_data(url)
        if res == -1:
            print(f'在重试了{RETRY_TIME}次之后依旧不能获取数据，跳过..')
            index += 1
            continue
        if res.status_code in code:
            print('页面不存在...')
            index += 1
            continue
        soup = BeautifulSoup(res.text, 'html.parser')
        print('成功获得数据...')
        # 处理数据，获取标签和点赞数
        tags = get_tags(soup.text)
        iine = get_like_count(soup.text)
        if iine < limit:
            print('点赞数不足要求，跳过...')
            index += 1
            continue

        # 判断是否存在tag
        tag_flag = False
        print('判断是否存在所需tag...')
        for i in TAGLIB:
            if i in tags:
                tag_flag = True
        print(tag_flag)
        if not tag_flag:
            print('没有所需tag...跳过')
            index += 1
            continue

        # 判断是否不可名状
        ds_flag = False
        for r in fatal_error:
            if r in tags:
                ds_flag = True
        print('正在判断是否位不可名状...')
        print(ds_flag)
        if ds == 0 and ds_flag:
            print("发现不可名状之物...")
            index += 1
            continue
        elif ds == 1 and not ds_flag:
            print("是正常世界...")
            index += 1
            continue
        elif ds == 1 and ds_flag:
            print('发现符合，正在获取图片链接...')
            img_url = get_img_url(soup.text)
            for t in range(RETRY_TIME):
                if dl(img_url, hash_name(get_ill_name(soup.text)), url) == 0:
                    print('下载完成...')
                    index += 1
                    write_index(index)
                    return index
                else:
                    index += 1
                    continue
        print('判断是否r18...')
        # 判断是否R18
        r18_flag = False
        for r in R18:
            if r in tags:
                r18_flag = True
        print(r18_flag)

        # 判断是否符合要求
        if r18 == 1:
            if r18_flag:
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
                            continue
                # else:
                #     print('存在R18但不存在所需标签，跳过...')
                #     index += 1
                #     continue
            else:
                print('不是R18，跳过...')
                index += 1
                continue
        elif r18 == 2:
            if tag_flag:
                if r18_flag:
                    print('存在R18，跳过')
                    index += 1
                    continue
                else:
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
                    index += 1
                    return index
        elif r18 == 3:
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
                index += 1
                return index
            # else:
            #     print('不存在所需标签，跳过...')
            #     index += 1
            #     continue
