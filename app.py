import dropbox, smtplib,os
from datetime import datetime
from email.mime.text import MIMEText

#VARIABLES
todayArray = []
weekArray =[]
timeNow= datetime.utcnow()
secDay = 86400
secWeek = 604800
api = os.environ['DROPBOX_API']
username = os.environ['DROPBOX_EMAIL_USER']
password = os.environ['DROPBOX_EMAIL_PASSWORD']

#initiating classes
dbx = dropbox.Dropbox(api)

# MAILER FUNCTION
def smtpMailer(todayArray,weekArray,username,password):
    #VARIABLES
    sender = 'bullhorn0002@gmail.com'
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

    msg = MIMEText("From: {0}\r\n To: {1}\r\n\r\n Files uploaded today: \r\n\r\n {2} \r\n\r\n Files uploaded this week: \r\n\r\n {3}".format(sender,receiver,todayStr,weekStr))
    msg['Subject'] = '{0} files uploaded today'.format(len(todayArray))
    msg['From'] = sender
    msg['To'] = receiver

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    print(msg)
    #server.sendmail(sender,receiver,msg.as_string())
    server.quit()

# STARTING APP
for entry in dbx.files_list_folder('/tax/work papers',recursive=True).entries:
    if hasattr(entry,'id'): #checking to ensure someone else uploaded it
        if entry.id != 'id:p_Z1dV08HFAAAAAAAAAAAQ':
            if hasattr(entry,'client_modified'): #ensuring it's a file
                timeDiff= timeNow - entry.client_modified
                if int(timeDiff.total_seconds()) < secDay:
                    todayArray.append([entry.path_lower.replace(" ","%20"),entry.client_modified])
                elif int(timeDiff.total_seconds()) < secWeek:
                    weekArray.append([entry.path_lower.replace(" ","%20"),entry.client_modified])
                else:
                    pass
        else:
            pass
    else:
        pass

smtpMailer(todayArray,weekArray,username,password)
