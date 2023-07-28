import time
import hashlib
from urllib.request import urlopen, Request
import smtplib
from email import message

def send_email(url):
    msg = message.Message()
    msg.add_header('from', 'pi@richardhartnell.com')
    msg.add_header('to', 'programming@lookoutarts.com')
    msg.add_header('subject', ('Website updated: ' + url))
    msg.set_payload('Hello! A little computer would like to let you know that ' + url + ' was recently updated.')
    server = smtplib.SMTP('smtp.dreamhost.com', 587)
    server.login('pi@richardhartnell.com', pwd)
    server.send_message(msg, from_addr='pi@richardhartnell.com', to_addrs='programming@lookoutarts.com')

from_addr = 'pi@richardhartnell.com'
to_addr = 'programming@lookoutarts.com'
hashes = {}

with open('./creds.txt', 'r') as password_file:
    pwd = password_file.read()

url_list = ['https://www.artsfund.org/accelerator/',
            'https://www.whatcomcf.org',
]

#create initial hashes
for url in url_list:
    response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read(9000)
    hashes[url] = hashlib.sha224(response).hexdigest()

send_email('test.com')
print("running")
print(hashes)
time.sleep(3)

# while True:
#     for url in url_list:
#         try:
#             # perform the get request and store it in a var
#             response = urlopen(url).read(9000)

#             # create a hash
#             currentHash = hashlib.sha224(response).hexdigest()

#             # wait for 30 seconds
#             time.sleep(3)

#             # perform the get request
#             response = urlopen(url).read(9000)

#             # create a new hash
#             newHash = hashlib.sha224(response).hexdigest()

#             # check if new hash is same as the previous hash
#             if newHash == currentHash:
#                 continue

#             # if something changed in the hashes
#             else:
#                 # notify
#                 send_email(url)

#                 #save new hash
#                 response = urlopen(url).read(9000)
#                 hashes[url] = hashlib.sha224(response).hexdigest()
#                 time.sleep(3)
#                 continue

#         except Exception as e:
#             print("error")
