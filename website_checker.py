import time
import hashlib
from urllib.request import urlopen, Request
import smtplib
from email import message

# global vars
from_addr = 'pi@richardhartnell.com'
hashes = {}
readlength = 9000
sleeptime = 5

#specialize this
to_addr = 'programming@lookoutarts.com'


def send_email(url):
    if url in laq_list:
        to_addr = 'programming@lookoutarts.com'
    else:
        to_addr = 'richard@richardhartnell.com'
    msg = message.Message()
    msg.add_header('from', 'pi@richardhartnell.com')
    msg.add_header('to', to_addr)
    msg.add_header('subject', ('Website updated: ' + url))
    msg.set_payload('Hello! A little computer would like to let you know that ' + url + ' was recently updated.')
    server = smtplib.SMTP('smtp.dreamhost.com', 587)
    server.login('pi@richardhartnell.com', pwd)
    server.send_message(msg, from_addr='pi@richardhartnell.com', to_addrs=to_addr)

# this is fine.
def make_hash(url):
    response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read(readlength)
    hashes[url] = hashlib.sha224(response).hexdigest()

def check_url(url):
    try:
        response = urlopen(url).read(readlength)
        newHash = hashlib.sha224(response).hexdigest()
        if newHash != hashes[url]:
            print("something changed: " + url)
            send_email(url)
            hashes[url] = newHash
            time.sleep(sleeptime)
        else:
            pass
    except Exception as e:
        print("error", e)

print("running")

with open('./creds.txt', 'r') as password_file:
    pwd = password_file.read()

laq_list = ['https://www.arts.wa.gov/grants/',
            'https://whatcomcf.org/receive/apply-for-a-grant/',
            'https://www.artsfund.org/about-arts-fund/grants/',
            'https://www.skagitcf.org/grantmaking.html'
]

chard_list = ['https://www.olark.com/jobs',
              'https://careers.prezly.com/',
]

#create initial hashes
for url in laq_list:
    make_hash(url)

for url in chard_list:
    make_hash(url)

print("first hashes complete")
time.sleep(sleeptime)

while True:
    for url in laq_list:
        check_url(url)
    for url in chard_list:
        check_url(url)