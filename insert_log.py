#!/usr/bin/python3
#author: justbio

import pymysql
import sys
import logging
import time

# get column data for db from argvs
def get_data():
    sendto = sys.argv[1]
    host = sys.argv[2]
    body = sys.argv[3]
    etime = body.split("\r\n")[0]
    detail = body.split("\r\n")[1]
    flag = 0
    return etime,host,detail,sendto,flag

# insert data to db
def insert_db(etime, host, detail, sendto, flag):
    conn = pymysql.connect(host="YOURDBHOST", user="YOURDBUSER", password="YOURDBPWD", db="YOURDBNAME")
    cursor = conn.cursor()
    check_table_sql = "show tables"
    cursor.execute(check_table_sql)
    tables = cursor.fetchall()
    tb_name = "logs" + time.strftime("%Y%m%d", time.localtime())
    if (tb_name,) not in tables:
        create_table_sql = "create table %s like template" % (tb_name)
        cursor.execute(create_table_sql)
    insert_sql = "insert into %s set time = '%s', host = '%s', detail = '%s', sendto = '%s', flag = %d" % (tb_name, etime, host, detail, sendto, flag)
    cursor.execute(insert_sql)
    conn.commit()
    conn.close()

def main():
    etime,host,detail,sendto,flag = get_data()
    try:
        insert_db(etime, host, detail, sendto, flag)
    except Exception as e:
        # error to write log
        logging.basicConfig(filename='/var/log/zabbix/insert_sql_err.log',format='%(asctime)s :%(levelname)s :%(message)s')
        logging.error("%s;%s;%s;%s" % (etime,host,detail,str(e)))

if __name__ == '__main__':
    main()
