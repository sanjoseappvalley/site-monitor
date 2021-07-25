import requests
import smtplib
import os
import time
from linode_api4 import LinodeClient, Instance
# import logging

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
site = 'https://immortalnovels.com'

# for linode in client.linode.instances():
# 	print(f'{linode.label}: {linode.id}')

# logging.basicConfig(filename='PATH_TO_DESIRED_LOG_FILE',
#                     level=logging.INFO,
#                     format='%(asctime)s:%(levelname)s:%(message)s')

def notify():
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

		subject = 'THE SITE IS DOWN'
		body = 'Make sure the server restarted and it is back up'
		msg = f'Subject: {subject}\n\n{body}'
		# logging.info('Sending Email...')
		smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

def reboot():
	client = LinodeClient(LINODE_TOKEN)
	myserver = client.load(Instance, 28344765)
	myserver.reboot()
	# logging.info('Attempting to reboot server...')

try:
	r = requests.get(site, timeout=5)
	if r.status_code != 200:
		# logging.info('Website is DOWN!')
		notify()
		reboot()
	else:
		# logging.info('Website is UP')
		print('Web is up')
		time.sleep(5)
except Exception as e:
	# logging.info('Website is DOWN!')
	notify()
	reboot()

# ~/site-monitor/virtualenv/Scripts/python ~/site-monitor/monitor.py
