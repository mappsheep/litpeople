#!/usr/bin/python
import subprocess
import urllib2

def wifi():
	try:
		urllib2.urlopen('https://www.google.com', timeout = 1)
		print ('Wifi is up')
		return True

	except urllib2.URLError as err:
		return False

tries = 0
while (wifi() == False):
	if (tries == 0):
		print ('This is the crontab wifi check, apparantly it is down')
		print ('This is a going to take a long second, running network restart')

	subprocess.call('/home/pi/People_Count/restartnet.sh')

	wifi()

	if (wifi() == True):
		print('It is live again')
		break
		
