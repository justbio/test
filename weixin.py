#!/usr/bin/python

import urllib,urllib2
import json
import sys

def gettoken(corpid,corpsecret):
    gettoken_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + corpsecret
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print e.code
        print e.read().decode("utf8")
        sys.exit()
    token_data = token_file.read().decode("utf-8")
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json["access_token"]
    return token

def senddata(access_token,party,content):
    send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
    send_values = {"touser":"","toparty":party,"msgtype":"text","agentid":"2","text":{"content":content },"safe":"0" }
    #agentid是公众号的应用ID
    send_data = json.dumps(send_values, ensure_ascii=False)
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print str(response)

if __name__ == "__main__":
    content = str(sys.argv[2])
    corpid = "xxxx" #公众号的corpid
    corpsecret = "xxxx" #公众号的corpsecret
    party = sys.argv[1]  #从zabbix传过来的公众号用户组的代码
    accesstoken = gettoken(corpid,corpsecret)
    senddata(accesstoken,party,content)