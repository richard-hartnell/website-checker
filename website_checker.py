import time
import hashlib
from urllib.request import urlopen, Request
import smtplib
from email import message

from_addr = 'pi@richardhartnell.com'
to_addr = 'programming@lookoutarts.com'
hashes = {}
readlength = 9000
sleeptime = 1800

def send_email(url):
    msg = message.Message()
    msg.add_header('from', 'pi@richardhartnell.com')
    msg.add_header('to', 'programming@lookoutarts.com')
    msg.add_header('subject', ('Website updated: ' + url))
    msg.set_payload('Hello! A little computer would like to let you know that ' + url + ' was recently updated.')
    server = smtplib.SMTP('smtp.dreamhost.com', 587)
    server.login('pi@richardhartnell.com', pwd)
    server.send_message(msg, from_addr='pi@richardhartnell.com', to_addrs='programming@lookoutarts.com')

def make_hash(url):
    response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read(readlength)
    hashes[url] = hashlib.sha224(response).hexdigest()

print("running")

with open('./creds.txt', 'r') as password_file:
    pwd = password_file.read()

url_list = ['https://www.arts.wa.gov/grants/',
            'https://whatcomcf.org/receive/apply-for-a-grant/',
            'https://www.artsfund.org/about-arts-fund/grants/'
]

#create initial hashes
for url in url_list:
    make_hash(url)

print("first hashes complete")
time.sleep(sleeptime)

while True:
    for url in url_list:
        try:

            response = urlopen(url).read(readlength)
            newHash = hashlib.sha224(response).hexdigest()

            if newHash == hashes[url]:
                continue

            else:
                print("something changed: " + url)
                send_email(url)
                hashes[url] = newHash
                time.sleep(sleeptime)
                continue

        except Exception as e:
            print("error")