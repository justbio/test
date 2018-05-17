#!/usr/local/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import sys,time,random

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
    path="C:/Users/vcc-admin/Documents/GitHub/test"
    mail_host="yourmailhost"
    mail_user="yourmailname"
    mail_pass="yourmailpassword"
    sender = 'yourmailaddress'
    receivers = get_to(sys.argv[1])
    subject = sys.argv[2]
    text = sys.argv[3]
    mailid = str(int(time.time())) + str(int(random.random() * 1000))
    for i in range(3):
        res = sendmail(mail_host,mail_user,mail_pass,sender,receivers,subject,text,mailid)
        if res == "success":
            break
        else:
            i += 1
            logging.warning("sendmail(mailid:%s) failed for %s times" % (mailid, str(i))

if __name__ == "__main__":
    main()