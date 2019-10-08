import os
import re

import requests, hashlib

TAGLIB = ['\\u30aa\\u30ea\\u30b8\\u30ca\\u30eb',  # オリジナル
          '\\u3075\\u3068\\u3082\\u3082',  # ふともも
          '\\u9b45\\u60d1\\u306e\\u3075\\u3068\\u3082\\u3082',  # 魅惑のふともも
          '\\u5973\\u306e\\u5b50',  # 女の子
          '\\u814b',  # 腋
          '\\u9280\\u9aea\\u30ed\\u30f3\\u30b0',  # 銀髪ロング
          '\\u9b45\\u60d1\\u306e\\u8c37\\u9593',  # 魅惑の谷間
          '\\u5de8\\u4e73',  # 巨乳
          '\\u6975\\u4e0a\\u306e\\u4e73',  # 極上の乳
          '\\u30a2\\u30ba\\u30fc\\u30eb\\u30ec\\u30fc\\u30f3',  # アズールレーン
          '\\u91cd\\u91cf\\u611f\\u3042\\u308b\\u3088\\u306a',  # 重量感あるよな
          '\\u30e9\\u30a4\\u30b6\\u306e\\u30a2\\u30c8\\u30ea\\u30a8',  # ライザのアトリエ # 莱莎的炼金工坊
          '\\u30e9\\u30a4\\u30b6\\u30ea\\u30f3\\u30fb\\u30b7\\u30e5\\u30bf\\u30a6\\u30c8',  # ライザリン・シュタウト  # 莱莎琳・斯托特
          '\\u5c3b\\u795e\\u69d8',  # 尻神様
          '\\u3061\\u3061\\u3057\\u308a\\u3075\\u3068\\u3082\\u3082',  # ちちしりふともも
          '\\u30d5\\u30a9\\u30fc\\u30df\\u30c0\\u30d6\\u30eb(\\u30a2'
          '\\u30ba\\u30fc\\u30eb\\u30ec\\u30fc\\u30f3)',  # フォーミダブル(アズールレーン)
          '\\u30d5\\u30a9\\u30fc\\u30df\\u30c0\\u30d6\\u30eb',  # フォーミダブル # 可畏
          '\\u80f8\\u819d\\u4f4d',  # 胸膝位
          'T\\u30d0\\u30c3\\u30af',  # Tバック
          '\\u3080\\u3061\\u3080\\u3061',  # むちむち
          '\\u6a2a\\u4e73',  # 横乳
          '\\u5317\\u534a\\u7403\/\\u5357\\u534a\\u7403',  # 北半球\/南半球 *有待测试
          '\\u30d0\\u30cb\\u30fc\\u30ac\\u30fc\\u30eb',  # バニーガール
          '\\u306b\\u3058\\u3055\\u3093\\u3058',  # にじさんじ
          '\\u30b5\\u30a4\\u30cf\\u30a4\\u30bd\\u30c3\\u30af\\u30b9',  # サイハイソックス # 长筒袜
          '\\u767d\\u4e0a\\u30d5\\u30d6\\u30ad',  # 白上フブキ
          '\\u30db\\u30ed\\u30e9\\u30a4\\u30d6',  # ホロライブ
          '\\u8266\\u3053\\u308c',  # 艦これ
          '\\u8266\\u968a\\u3053\\u308c\\u304f\\u3057\\u3087\\u3093',  # 艦隊これくしょん
          '\\u7db2\\u30bf\\u30a4\\u30c4',  # 網タイツ
          '\\u9280\\u9aea',  # 銀髪
          '\\u9ed1\\u4e1d\\u889c',  # 黑丝袜
          '\\u9ed2\\u30b9\\u30c8',  # 黒スト
          # TODO 可能写个自动化自动添加热度高的tag，但是目前大概就这样了，后续会开放自定义tag的功能
          ]
R18 = 'R-18'


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
        req = requests.get(url, headers=header, timeout=(10, 30))
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
mark_file = './index.txt'

def get_index():
    """
    获取下一个可以爬取的序号
    :return: str
    """
    with open(mark_file, 'r') as f:
        line = f.readline()
    f.close()
    return line


def create_index(start=0):
    """
    创建进度
    :param start: 开始网页序号
    """
    with open(mark_file, 'w') as f:
        f.write(str(start) + '\n')
    f.close()


''' 弃用
def get_allindex():
    """
    获取当前所有进度
    :return: list
    """
    index = []
    with open('mark_file', 'r') as f:
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
    with open(mark_file, 'w') as f:
        f.write(str(index) + '\n')
    f.close()
