import re

url = r"u'In <a href=\"https://www.dropbox.com/home/tax/work%20papers/romeo/Rusu/Dans%20Tax%20Documents\" target=\"_blank\">Dans Tax Documents</a>, Daniel rusu added the file <a href=\"https://www.dropbox.com/event_details/14433446/1348297075/579248503/0\" target=\"_blank\">electrical-licloc.txt</a>.<br />'"
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)

print(urls)
