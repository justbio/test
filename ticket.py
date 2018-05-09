#!/use/bin/python3
#Author:justbio
from otrs.ticket.template import GenericTicketConnectorSOAP
from otrs.client import GenericInterfaceClient
from otrs.ticket.objects import Ticket, Article, DynamicField, Attachment
import sys

def access_otrs(user,passwd):
    server_uri = r'http://192.168.0.193'
    webservice_name = 'GenericTicketConnectorSOAP'
    client = GenericInterfaceClient(server_uri, tc=GenericTicketConnectorSOAP(webservice_name))
    client.tc.SessionCreate(user_login=user, password=passwd)
    return client

def open_ticket(title,body,typeid,queue,eventid,client):
    t = Ticket(State='open', Priority='3 normal', Queue=queue,
        Title=title, CustomerUser='zabbix',
        TypeID=typeid)
    a = Article(Subject=title, Body=body, Charset='UTF8',
        MimeType='text/plain')
    df1 = DynamicField(Name='EventID', Value=eventid)
    t_id, t_number = client.tc.TicketCreate(t, a, [df1])

def search_ticket(eventid,client):
    df1 = DynamicField(Name='EventID', Value=eventid,Operator="Equals")
    tickets = client.tc.TicketSearch(dynamic_fields=[df1])
    return tickets[0]

def recovery_article(title,body,eventid,client):
    ticket = search_ticket(eventid,client)
    new_article = Article(Subject=title, Body=body, Charset='UTF8',MimeType='text/plain')
    client.tc.TicketUpdate(ticket, article=new_article)

def close_ticket(eventid,client):
    ticket = search_ticket(eventid,client)
    t_upd = Ticket(State='closed successful')
    client.tc.TicketUpdate(ticket, ticket=t_upd)

def main():
    user=YOURUSERNAME
    passwd=YOURPASSWORD
    sendto={"server":"服务器队列","network":"网络队列"}
    queue=sendto[sys.argv[1]]
    title=sys.argv[2]
    body=sys.argv[3]
    if body.split("\n")[3].split()[1]=="Disaster":
        typeid="3"
    else:
        typeid="2"
    eventid=body.split("\n")[4].split()[1]
    client=access_otrs(user,passwd)
    if title.startswith("Problem"):
        open_ticket(title,body,typeid,queue,eventid,client)
    elif title.startswith("Resolved"):
        recovery_article(title,body,eventid,client)
        close_ticket(eventid,client)

if __name__ == '__main__':
    main()