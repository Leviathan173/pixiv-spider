import os
import re

import requests, hashlib


def to_unicode(string):
    """编码转换unicode
    :param string: 任意字符串
    :return: str
    """
    ret = ''
    for v in string:
        ret = ret + hex(ord(v)).lower().replace('0X', '\\u')

    return ret


def hash_name(string):
    return hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()


def get_like_count(data):
    """
    获取点赞数
    :param data: 网页数据
    :return: int
    """
    reg = re.compile(r"(?<=\"likeCount\":)\d+")
    like = reg.search(data)
    return int(like.group(0))


def get_ill_name(data):
    """
    获取插画的名称用以命名下载图片
    具体为，插画id:作品名
    :param data: 网页数据
    :return: str
    """
    title = re.findall('illustTitle\":\".*?\"', data)
    illustId = re.findall('illustId\":\".*?\"', data)
    return illustId[0].split(':')[1].split('"')[1] + ':' + title[0].split(":")[1].split('"')[1]


def get_img_url(data):
    """
    获取图片地址
    :param data: 网页数据
    :return: str
    """
    img = re.findall('\"regular\":\".*?\"', data)
    # print(img.split(':"')[1].split('"')[0].replace('\\', ''))
    return img[0].split(':"')[1].split('"')[0].replace('\\', '')


def get_tags(data):
    """
    获取图片tag
    :param data: 网页数据
    :return: list
    """
    tag = []
    tags = re.findall('\"tag\":\".*?\"', data)
    for i in tags:
        tag.append(i.split(':')[1].split('"')[1])
    return tag


def dl(url, name, ref, path='./img/'):
    """
    下载图片
    :param url: 图片地址
    :param name: 图片名字
    :param path: 本地存放路径
    """
    header = {
        'referer': ref,
    }
    if not os.path.exists(path):
        print('创建图片保存目录')
        os.mkdir(path)
    else:
        print('目录存在...')
    full_path = path + '{}.jpg'.format(name)
    try:
        req = requests.get(url, headers=header)
        print('获取文件成功...')
    except:
        print('获取文件失败...')
        print(f'准备获取的图片的地址为：{url}')
        return -1
    with open(full_path, 'wb') as f:
        f.write(req.content)
    f.close()
    return 0


'''自动化模块
每次开始都会创建进度，进度每X次自动更新(往上累加X次)，X取决于increase_num的大小
每次爬取都会读取进度的首条，无论该页是否能够访问，无论是否符合条件，爬取之后都会删除此条进度
'''

increase_num = 10000


def get_index():
    """
    获取下一个可以爬取的序号
    :return: str
    """
    with open('./init.cfg', 'r') as f:
        line = f.readline()
    f.close()
    return line


def create_index(start=0):
    """
    创建进度
    :param start: 开始网页序号
    """
    with open('./init.cfg', 'w') as f:
        f.write(str(start) + '\n')
    f.close()


''' 弃用
def get_allindex():
    """
    获取当前所有进度
    :return: list
    """
    index = []
    with open('./init.cfg', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            index.append(line)
    f.close()
    return index
'''


def write_index(index):
    """
    写入进度
    :param index: 进度页面编号
    """
    with open('./init.cfg', 'w') as f:
        f.write(str(index)+'\n')
    f.close()
