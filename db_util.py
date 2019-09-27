import mysql.connector
import time
from db_init import get_conn


def add_(url, dl_rul, conn):
    cursor = conn.cursor(buffered=True)
    try:
        sql = 'insert into erogazo(url,timestamp,download_url) values(%s,%s,%s)'
        data = []
        for i in range(len(url)):
            tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            data.append((url[i], tt, dl_rul[i]))
        cursor.executemany(sql, data)
        print('成功插入{}条数据...'.format(len(url)))
    except mysql.connector.Error as e:
        print('插入数据出错：', str(e))

