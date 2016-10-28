Use dropbox get_folders api call to get a list of entries in the appropriate folder. Then put all that in a csv file that is then emailed to the client.

Make this a simple script on my site that the client can visit and can click to run when they choose

KEYWORDS:
    get_folders
    list of entries
    csv file
    email - smtp
    cron scheduled
    file versus folder


SUDO:

init todayArray
init weekArray
init datetime now

for each entry in files_list_folder:
    if has client_modified (file)
        if datetimenow - client_modified < 24 hours
            add to todayArray
        else if datetimenow - client_modified < 168 hours
            add to weekArray
        else
            pass
send arrays to smtp function

def smtpmailer(todayArray,weekArray):
    send email with the 2 arrays printed out.
