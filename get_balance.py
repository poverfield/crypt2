# kraken accunt balance
# Run on the 1,16 of each month

import ccxt
import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# set working directory in raspberry
path = '/home/pi/Desktop/files'
os.chdir(path)

# read in private information
f = open('account.txt') # read in account.txt
f_lines = f.readlines()
email = f_lines[0].split(': ',1)[1][0:len(f_lines[0].split(': ',1)[1])-1] # email address (send and recieve)
email_password = f_lines[1].split(': ',1)[1][0:len(f_lines[1].split(': ',1)[1])-1] # aocapital1@gmail.com password
api_key = f_lines[2].split(': ',1)[1][0:len(f_lines[2].split(': ',1)[1])-1] # kraken api key
api_secret = f_lines[3].split(': ',1)[1] # kraken api secret
f.close()

# connect to kraken
kraken = ccxt.kraken()
kraken.apiKey = api_key
kraken.secret = api_secret

balance = kraken.fetchBalance()
usd = round(balance['USD']['total'],2)
eth = balance['ETH']['total']

# get open orders
open_order = len(kraken.fetchOpenOrders())

# date
now = str(datetime.datetime.now())
now_date = now[0:10]

# email
def send_email(usd,  delt): 
    print('Sending...')
    sender = email
    receiver = email
    password = email_password

    msg = MIMEMultipart()
    msg['Subject'] = 'Account Balance'
    msg['From'] = sender
    msg['To'] = receiver

    disclaimer = '''The above percent change assumes that no funds have been deposited/withdrawn from your account during this 15-day period. \n
If there have been then this value is not correct.\n
Additionally, no open positions are included in the 'Percent Change' value.'''
    message = message = 'Date: ' + now_date + '\n\n' + 'Account Balance: $' + str(usd) + '\n\n' + 'Percent Change: ' + str(delt) + ' %' + '\n\n\n' + 'Disclaimer: ' + disclaimer
    msg.attach(MIMEText(message))
    s = server = smtplib.SMTP('smtp.gmail.com:587') #smtp.gmail.com:587
    s.starttls()
    s.login(sender, password)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    print('Sent.')

# read in old balance
f = open('balance.txt')
f_lines = f.readlines()
balance_old = round(float(f_lines[0]),2)
f.close()

# percent change
delt = round((usd/balance_old -1)*100,2)

# email
send_email(usd, delt)

# write out new balance
print('write balance to usd')
f = open('balance.txt', 'w')
f.write(str(usd))
f.close()






    
