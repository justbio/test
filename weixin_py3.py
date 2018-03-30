#!/usr/bin/python3

import urllib.request
import json
import sys

#default for zabbix2.x, or zabbix3.x witch set action's (to=$1,subject=$2,body=$3)

def gettoken(corpid,corpsecret):
    gettoken_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + corpsecret
    try:
        token_file = urllib.request.urlopen(gettoken_url)
    except urllib.request.HTTPError as e:
        print (e.code)
        print (e.read().decode("utf8"))
        sys.exit()
    token_data = token_file.read().decode("utf-8")
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json["access_token"]
    return token

def senddata(access_token,party,content,agentid):
    send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
    #agentid
    send_values = {"touser":"","toparty":party,"msgtype":"text","agentid":agentid,"text":{"content":content },"safe":"0" }
    data = json.dumps(send_values, ensure_ascii=False)
    send_data=bytes(data,'utf8')
    send_request = urllib.request.Request(send_url)
    response = urllib.request.urlopen(send_request,send_data).read()
    print (str(response))

if __name__ == "__main__":
    content = str(sys.argv[3])
    agentid = "xxxx" #application agentid
    corpid = "xxxx" #corpid
    corpsecret = "xxxx" #corpsecret
    party = sys.argv[1]  #zabbix alert subject
    accesstoken = gettoken(corpid,corpsecret)
    senddata(accesstoken,party,content,agentid)