# encoding:utf-8
import requests
import os


def dl(url, index, path='./img/'):
    if os.path.exists(path):
        print('创建图片保存目录')
        os.mkdir(path)
    full_path = path + '{}.jpg'.format(index)
    req = requests.get(url)
    print('获取文件成功...')
    with open(full_path, 'wb') as f:
        f.write(req.content)
    f.close()
