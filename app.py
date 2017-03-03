# test to see how many entries come back

# !/usr/bin/env python2.7

import dropbox, smtplib,os,sendgrid
from datetime import datetime
from email.mime.text import MIMEText
from sendgrid.helpers.mail import *

# VARIABLES
lastHourArray = []
todayArray = []
currentTime = datetime.utcnow()
api = os.environ['DROPBOX_API']
username = os.environ['DROPBOX_EMAIL_USER']
password = os.environ['DROPBOX_EMAIL_PASSWORD']
sendGridApi = os.environ['SENDGRID_API']
dbx = dropbox.Dropbox(api)
entriesTotalArray = []
sender = 'dan@deliveredads.com'
receiver = 'me@brianlang.tax''

# MAILER FUNCTION
def smtpMailer(lastHourArray,todayArray,username,password,sendGridApi):
    lastHourStr = ''
    count = 1
    for item in lastHourArray:
        lastHourStr +=  '#{0} File edited: '.format(str(count))
        lastHourStr += str(item[0])
        lastHourStr += ' url: '
        lastHourStr += item[1]
        lastHourStr += ' at: '
        lastHourStr += item[2]
        lastHourStr += '\r\n'
        count += 1

    todayStr = ''
    count = 1
    for item in todayArray:
        todayStr +=  '#{0} File edited: '.format(str(count))
        todayStr += str(item[0])
        todayStr += ' url: '
        todayStr += item[1]
        todayStr += ' at: '
        todayStr += item[2]
        todayStr += '\r\n'
        count += 1

    msg = "<b>Files uploaded last hour:</b> \r\n\r\n\r\n\r\n {2} <b>Other Files uploaded today (not including last hour):</b> \r\n\r\n {3} \r\n\r\n".format(sender,receiver,lastHourStr,todayStr)
    sg = sendgrid.SendGridAPIClient(apikey=sendGridApi)
    from_email = Email(sender)
    subject = '{0} files uploaded in last hour'.format(len(lastHourArray))
    to_email = Email(receiver)

    content = Content("text/plain", msg)

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print('Sent to: ' + receiver)
    print(response.status_code)
    print(response.body)
    print(response.headers)

entries = dbx.files_list_folder('/brian alan lang ea/work papers/',recursive=True)
entriesTotalArray.extend(entries.entries)

if entries.has_more:
    count = 1
    while True:
        entries = dbx.files_list_folder_continue(entries.cursor)
        entriesTotalArray.extend(entries.entries)
        if entries.has_more:
            count += 1
            print('on: ' + str(count))
        else:
            break

for entry in entriesTotalArray:
    if hasattr(entry, 'client_modified'):
        if str(entry.sharing_info.modified_by) != 'dbid:AACSi6iUvmmK0JGy2X3DPFKuqrRsgp2l8jQ': # his user id
            dateModified = entry.client_modified
            minDifference = (currentTime - dateModified).total_seconds() / 60
            if minDifference < 60:
                lastHourArray.append([str(entry.name),'https://www.dropbox.com/home' + str(entry.path_lower), entry.client_modified.strftime("%Y-%m-%d %H:%M:%S")])
            elif minDifference < 1440:
                todayArray.append([str(entry.name),'https://www.dropbox.com/home' + str(entry.path_lower.replace(' ','%20')), entry.client_modified.strftime("%Y-%m-%d %H:%M:%S")])

print('last hour array')
print(lastHourArray)

print('today array')
print(todayArray)

if lastHourArray:
    smtpMailer(lastHourArray,todayArray,username,password,sendGridApi)
