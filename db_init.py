# encoding:utf-8
import mysql.connector
import re


def get_conn():
    config = {
        'host': '123.207.101.171',
        'user': 'ankai',
        'password': 'Ankai@1999',
        'auth_plugin': 'mysql_native_password',
        'port': '3306',
        'database': 'A_spider',
        'charset': 'utf8',
    }
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print(e)
    else:
        print('connect success')
        return conn


def is_table_created(conn):
    sql = 'show tables'
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if len(table_list) > 0:
        return True
    else:
        return False


def init(connection):
    if is_table_created(connection):
        print('表已存在,跳过...')
        return 1
    else:
        sql_create_table = 'create table `erogazo`' \
                           '(`id` int(10) not null auto_increment,' \
                           '`url` varchar(200) not null,' \
                           '`timestamp` timestamp not null,' \
                           '`download_url` varchar(400) not null,' \
                           'primary key(`id`))'
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute(sql_create_table)
            print('创建表成功...')
            return 0
        except mysql.connector.Error as e_table:
            print('创建表失败...', str(e_table))
            return -1


def main():
    conn = get_conn()
    i = init(conn)
    if i == 0:
        print('初始化数据库成功...')
    elif i == 1:
        print('不需要初始化...')
    else:
        print('初始化失败...')
    conn.close()


if __name__ == '__main__':
    main()
