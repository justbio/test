#!/usr/local/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import sys,time,random

# mkdir script_path/logs/, will create log file by date automaticly.
def logging(path,log):
    today = time.strftime("%Y%m%d", time.localtime())
    with open(path + "/logs/sendmail" + str(today) +".log","a+") as f:
        f.write(log)

# mkdir script_path/logs/, and write addresslist by format :xxx@xxx.xx,xxx@xxx.xx
def get_to(path,to):
	with open(path + "/addresslist/" + to +".txt","r") as f:
		line = f.readline()
		receivers = line.split(",")
	return receivers

def sendmail(path,mail_host,mail_user,mail_pass,sender,receivers,subject,text,mailid):
    message = MIMEMultipart()
    message['From'] = Header("zabbix", 'utf-8')
    message['To'] =  Header("operator", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        smtpObj = smtplib.SMTP(mail_host, 587)
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        log = now + " sendmail successful(mailid:" + mailid + ") \n    mail_to:" + ','.join(receivers) + "\n    subject:" + subject + "\n    " + text +"\n"
        logging(path,log)
        res= "success"
    except smtplib.SMTPException as e:
        log = now + " sendmail failed(mailid:" + mailid + ") \n    "  + str(e) +"\n    mail_to:" + ','.join(receivers) + "\n    subject:" + subject + "\n    " + text +"\n"
        res = "failed"
        logging(path,log)
    return res

def main():
    path="C:/Users/vcc-admin/Documents/GitHub/test"
    mail_host="yourmailhost"
    mail_user="yourmailname"
    mail_pass="yourmailpassword"
    sender = 'yourmailaddress'
    receivers = get_to(path,sys.argv[1])
    subject = sys.argv[2]
    text = sys.argv[3]
    mailid = str(int(time.time())) + str(int(random.random() * 1000))
    for i in range(3):
        res = sendmail(path,mail_host,mail_user,mail_pass,sender,receivers,subject,text,mailid)
        if res == "success":
        	break
        else:
        	i += 1
        	logging(path,"    Failed For " + str(i) + " Time\n")

if __name__ == "__main__":
	main()