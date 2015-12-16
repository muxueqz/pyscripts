#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import os
import outbox
import argparse
#import optparse

 
if __name__ == "__main__":
#    usage = "usage: %prog [options] arguments"
#    parser = optparse.OptionParser(usage)
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--subject", dest="subject", help="Subject")   
    parser.add_argument("-f", "--from", dest="email_from", help="From")   
#    parser.add_argument("-t", "--to", dest="email_to", help="To", action='append')
    parser.add_argument("-t", "--to", dest="email_to", help="To", nargs='+')
    parser.add_argument("-c", "--content", dest="content", help="The content file")   
    parser.add_argument("-p", "--password", dest="password", help="Password")   
    parser.add_argument("-u", "--user", dest="user", help="User")   
    parser.add_argument("-S", "--server", dest="server", help="SMTP Server")   
    parser.add_argument("-a", "--attfile", dest="attfiles")   

#    (options, args) = parser.parse_args()
    options = parser.parse_args()

    content = open(options.content).read()

#    sendMail(
#            options.email_from, 
#            [options.email_to], 
#            options.subject, content, 
#            [options.attfiles] 
#        ) 

    port = 25

    try:
        port = options.server.split(':')[1]
        options.server = options.server.split(':')[0]
    except:
        pass

    o = outbox.Outbox(username=options.user,password=options.password,server=options.server,port=port,mode='TLS')
#    o.send(outbox.Email(subject=options.subject,body=content,recipients=[options.email_to]))
    atts = [outbox.Attachment(os.path.basename(options.attfiles),fileobj=open(options.attfiles,'rb'))]
    o.send(outbox.Email(subject=options.subject,body=content,recipients=options.email_to),attachments=atts)
    print 'Mail Send Success'
