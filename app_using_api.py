#!/usr/bin/env python2.7

import dropbox, smtplib,os,sendgrid
from datetime import datetime
from email.mime.text import MIMEText
from sendgrid.helpers.mail import *

#VARIABLES
todayArray = []
weekArray =[]
timeNow= datetime.utcnow()
secDay = 86400
secWeek = 604800
api = os.environ['DROPBOX_API']
username = os.environ['DROPBOX_EMAIL_USER']
password = os.environ['DROPBOX_EMAIL_PASSWORD']
sendGridApi = os.environ['SENDGRID_API']


# MAILER FUNCTION
def smtpMailer(dbx, todayArray,weekArray,username,password):
    #VARIABLES
    sender = 'dan@deliveredads.com'
    receiver = 'daniel7rusu@gmail.com'
    #receiver = 'me@brianlang.tax'

    #ARRAYS TO STRING
    todayStr = ''
    weekStr = ''
    if not todayArray:
        todayStr = 'Nothing for today'
    else:
        for item in todayArray:
            todayStr +=  'https://www.dropbox.com/home'
            todayStr += str(item[0])
            todayStr += ' on '
            todayStr += item[1].strftime("%B %d, %Y, %H:%M")
            todayStr += '\r\n'
    if not weekArray:
        weekStr = 'Nothing for this week'
    else:
        for item in weekArray:
                weekStr +=  'https://www.dropbox.com/home'
                weekStr += str(item[0])
                weekStr += ' on '
                weekStr += item[1].strftime("%B %d, %Y, %H:%M")
                weekStr += '\r\n'

    msg = "From: {0}\r\n To: {1}\r\n\r\n Files uploaded today: \r\n\r\n {2} \r\n\r\n Files uploaded this week: \r\n\r\n {3}".format(sender,receiver,todayStr,weekStr)

    sg = sendgrid.SendGridAPIClient(apikey=sendGridApi)
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
    #initiating classes
    dbx = dropbox.Dropbox(api)

    # STARTING APP
    for entry in dbx.files_list_folder('/tax/work papers',recursive=True).entries:
        if hasattr(entry,'id'): #checking to ensure someone else uploaded it
            if entry.id != 'id:p_Z1dV08HFAAAAAAAAAAAQ':
                if hasattr(entry,'client_modified'): #ensuring it's a file
                    timeDiff= timeNow - entry.client_modified
                    if int(timeDiff.total_seconds()) < secDay:
                        todayArray.append([entry.path_lower.replace(" ","%20"),entry.client_modified])
                        print(todayArray)
                    elif int(timeDiff.total_seconds()) < secWeek:
                        weekArray.append([entry.path_lower.replace(" ","%20"),entry.client_modified])
                        print(weekArray)
                    else:
                        pass
            else:
                pass
        else:
            pass

    smtpMailer(dbx, todayArray,weekArray,username,password)
