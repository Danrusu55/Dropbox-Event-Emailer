#!/usr/bin/env python2.7

import feedparser, smtplib,os,sendgrid,re
from datetime import datetime
from email.mime.text import MIMEText
from sendgrid.helpers.mail import *

# MAILER FUNCTION
def smtpMailer(todayArray,username,password,SendGridAPI):
    #ARRAYS TO STRING
    todayStr = ''
    if not todayArray:
        todayStr = 'Nothing for today'
    else:
        for item in todayArray:
            todayStr +=  'File uploaded into folder: '
            todayStr += str(item[0])
            todayStr += ' on '
            todayStr += item[1] #.strftime("%B %d, %Y, %H:%M")
            todayStr += '\r\n'

    msg = "From: {0}\r\n To: {1}\r\n\r\n Files uploaded today: \r\n\r\n {2} \r\n\r\n".format(sender,receiver,todayStr)
    sg = sendgrid.SendGridAPIClient(apikey=SendGridAPI)
    from_email = Email(sender)
    subject = '{0} files uploaded today'.format(len(todayArray))
    to_email = Email(receiver)
    content = Content("text/plain", msg)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == "__main__":
    #VARIABLES
    sender = 'dan@deliveredads.com'
    receiver = 'daniel7rusu@gmail.com'
    #receiver = 'me@brianlang.tax'
    print('Sent to: ' + receiver)
    todayArray = []
    timeNow= datetime.utcnow()
    SendGridAPI = os.environ['SENDGRID_API']
    username = os.environ['DROPBOX_EMAIL_USER']
    password = os.environ['DROPBOX_EMAIL_PASSWORD']

    # GET OBJECT
    entries = feedparser.parse('https://www.dropbox.com/14433446/22509204/ZV2nIyu2Il19ufIzPMJUAbpwrpd86qmor0RCh0wY/events.xml').entries

    # LOOP THROUGH, IF NOT POSTED BY HIM, APPEND THE STUFF TO THE ARRAY
    for entry in entries:
        if "You" not in entry.title:
            summary = entry.summary_detail.value
            if "folder" not in summary:
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', entry.summary_detail.value)[0]
                print(url)
                date = entry.updated
                todayArray.append([url,date])
    smtpMailer(todayArray,username,password,SendGridAPI)
    #print(todayArray)
