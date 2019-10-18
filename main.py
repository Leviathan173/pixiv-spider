# encoding:utf-8
import argparse
import os
import time

from util import *
import spider

parser = argparse.ArgumentParser(description='涩图获取器 v0.1c by Leviathan173')
parser.add_argument('-i', '--index', help='需要爬取的页面的开始序号，默认77100000', type=int)
parser.add_argument('-l', '--limit', help='最小被人喜欢的数值，只会爬取超过这个数值的涩图', type=int)
parser.add_argument('-r18', help='是否只抓取涩图,1=是,2=否,3=我全都要', type=int)
parser.add_argument('-ds', '--darkside', help='可怕的，不被大众接受的，那些你不会告诉别人的爱好，上帝不会原谅你的,0=关闭,1=开启', type=int)
parser.add_argument('-n', '--num', help='要爬取多少张图片', type=int)
# TODO 添加数据库选项支持
# 目前不知道怎么做匿名数据库支持，
# parser.add_argument('-db', help='是否使用数据库, yes or no')

DEFAULT_INDEX = 77100000
DEFAULT_LIMIT = 80

args = parser.parse_args()
print(args)
if args.index is not None:
    index = args.index
    create_index(index)
elif os.path.exists(mark_file):
    index = int(get_index())
else:
    index = DEFAULT_INDEX
    create_index()
print('index = {}'.format(index))
if args.limit is None:
    limit = DEFAULT_LIMIT
    print('no specific argument given, ues default value 300 for limit')
else:
    limit = args.limit
    print('limit={}'.format(limit))

if args.r18 is None:
    r18 = 3
    print('no specific argument given, ues default value True for r18')
else:
    r18 = args.r18
    print('r18={}'.format(r18))
print(type(args.r18))

if args.num is None:
    num = 200
    print('no specific argument given, ues default value 200 for times')
else:
    num = args.num
    print('times={}'.format(num))

if args.darkside is None:
    ds = 0
    print("it's still be good")
else:
    ds = args.darkside
    print(f'ds = {ds}')


def main():
    print('载入中...')
    time.sleep(3)
    ind = index
    for i in range(num):
        ind = spider.spider(ind, r18, limit, ds)


if __name__ == '__main__':
    main()
