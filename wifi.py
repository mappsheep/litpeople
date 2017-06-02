import subprocess

#connection = urllib2.Request('https://www.google.com')
#littyornah = urllib2.urlopen('https://www.google.com')

#try: littyornah

#except:
#	print('damn')
#	subprocess.call[('/home/pi/People_Count/forcewifi.sh')]

#if not littyornah:
#	print('awwwwww snap')
#
#if littyornah:
#	print("It's live in here")

#yha = subprocess.call[("echo", "litty as joint")]

#host = 'www.google.com'

#lit = subprocess.Popen(['ping', '-c 2', host], stdout = subprocess.PIPE)

#output = lit.communicate()[0]

#stringer = str(output)

#if (stringer == 'ping: unknown host www.google.com\n'):
#	print ('darn')

#wow = subprocess.check_output('ping: unknown host www.google.com')
#print wow

#subprocess.call('/home/pi/People_Count/forcewifi.sh', shell=True)

#output = Popen(stdout=PIPE, "ping", "google.com", shell=False)
#print output

#subprocess.check_call(["ping", "google.com"])
#subprocess.check_call("exit 1", shell=True)

import urllib2

#def internet_on():
   # try:
    #    urllib2.urlopen('https://www.google.com', timeout=1)
   #     return True
  #  except urllib2.URLError as err: 
 #       return False

#print internet_on()

def internet_on():
	try:
		urllib2.urlopen('https://www.google.com', timeout=1)
		return True
   
	except urllib2.URLError as err:
		return False

print internet_on()

if internet_on() == False:
	print ('okay we are working')
	subprocess.call('/home/pi/People_Count/getthewifi.sh')
