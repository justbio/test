#!/usr/bin/python3
#author:justbio

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import sys
import time
import random
import logging
import pymysql

# init logging config.
day = time.strftime("%Y-%m-%d", time.localtime())
logging.basicConfig(filename='/var/log/zabbix/sendmail-%s.log' % (str(day)),
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(message)s')

# mkdir script_path/addresslist/, and write addresslist by format :xxx@xxx.xx,xxx@xxx.xx
def get_to(to):
    with open("/usr/lib/zabbix/alertscripts/addresslist/" + to ,"r") as f:
        line = f.readline()
        receivers = line.split(",")
    return receivers

# get_data from mysql if flag=0,and set flag=1
def get_data(host, user, passwd, db):
    conn = pymysql.connect(host=host, user=user, password=passwd, db=db)
    cursor = conn.cursor()
    check_table_sql = "show tables"
    cursor.execute(check_table_sql)
    tables = cursor.fetchall()
    day = time.strftime("%Y%m%d", time.localtime())
    table = ("logs" + day ,)
    if table not in tables:
        return 0
    else:
        get_data_sql = "select * from %s where flag=0 order by sendto" % (table)
        cursor.execute(get_data_sql)
        data = cursor.fetchall()
        update_data_sql = "update %s set flag=1 where flag=0" % (table)
        cursor.execute(update_data_sql) 
        conn.commit()
        return data
    conn.close()

# set data from mysql to dict:{to1:log1\nlog2\nlog3\n,to2:log1\nlog2\nlog3\n}
def set_data(data):
    datadict={}
    for elem in data:
        key=elem[3]
        if key in datadict:
            datadict[key]+=("%s, %s, %s\n" % (elem[0],elem[1],elem[2]))
        else:
            datadict[key]=("%s, %s, %s\n" % (elem[0],elem[1],elem[2]))
    return datadict

# sendmail
def sendmail(mail_host,mail_user,mail_pass,sender,receivers,subject,text,mailid):
    message = MIMEMultipart()
    message['From'] = Header("zabbix", 'utf-8')
    message['To'] =  Header("operator", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP(mail_host, 587)
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        log = "sendmail successful(mailid:%s)\nmail_to:%s\nsubject:%s\n%s\n" % (mailid,','.join(receivers),subject,text)
        logging.info(log)
        res= "success"
    except smtplib.SMTPException as e:
        log = " sendmail failed(mailid:%s)\nmail_to:%s\nsubject:%s\n%s\n" % (mailid,','.join(receivers),subject,text)
        logging.info(log)
        res = "failed"
    return res

def main():
	# mysql config
    host = "YOURDBHOST"
    user = "YOURDBUSER"
    passwd = "YOURDBPWD"
    db = "YOURDBNAME"
    data = get_data(host, user, passwd, db)
    datadict = set_data(data)
    # send mail config
    mail_host="YOURSMTPHOST"
    mail_user="YOURMAILADDRESS"
    mail_pass="YOURMAILPWD"
    sender="YOURMAILADDRESS"
    subject = "server error log recieved"
    # set sendto address and body text
    for k,v in datadict.items():
        sendto = k
        text = """
Dear all:

We have recieved error log from zabbix sever,
detail:
%s
please check
        """ % (v)
        receivers = get_to(sendto)
        mailid = str(int(time.time())) + str(int(random.random() * 1000))
        # try 3 times
        for i in range(3):
            res = sendmail(mail_host,mail_user,mail_pass,sender,receivers,subject,text,mailid)
            if res == "success":
                break
            else:
                i += 1
                logging.warning("sendmail(mailid:%s) failed for %s times" % (mailid, str(i))

if __name__ == "__main__":
    main()

