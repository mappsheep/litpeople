#pulling all the necessary libraries
import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import MySQLdb
import urllib2

#making sure there is wifi, if no wifi then run script getthewifi to get wifi LOOOOL, the program is trying to open www.google.com
#if the wifi is down then the while loop will force wifi connect, to continue to loop until google is pingable
#the loop will try to give internet access for 3 tries after that it will leave the loop can continue execution
#if you know there will be no access, the loop will take about 2-5 minutes
#also if having trouble try 'sudo systemctl daemon-reload', this message will pop up after 'sudo service networking start' if the $
# $ system thinks you should do this
print ('Can you connect to the world wide web?')
def internet_on():
	try:
		urllib2.urlopen('https://www.google.com', timeout = 1)
		print ('Yes')
		subprocess.call('/home/pi/People_Count/sendemail.sh')
		return True

	except urllib2.URLError as err:
		print ('No')
		return False

tries = 0
while (internet_on() == False):
	tries += 1

	if (tries < 4):
		print 'This is try number: ', tries

	print ('Running "getthewifi" script')
	subprocess.call('/home/pi/People_Count/getthewifi.sh')

	print ('Now about to try and pull up google.com')
	print ('Are you connected?')

	internet_on()

	if (internet_on() == True):
		print ('You are now connected')
		print ('Proceeding to continue code execution')
		break

	if (tries == 3 and internet_on() == False):
		print ('Having continous access problems, check config files or DNS access')
		print ('Going to move on to rest of program without internet access...')
		print ('Maybe ctrl + C and try "sudo systemctl daemon-reload"')
		break

	print ('No dice, trying again....')

#connecting to the database on phpmyadmin, setting up cursor for outputing to database
print('Connecting to the phpmyadmin local database using mysql and setting up the cursor')
database = MySQLdb.connect(user = 'root', passwd = 'scottyfresh', db = 'people', host = 'localhost', port = 3306)
cursor = database.cursor()

#setting up the pins for data recieve
print('Initializing the pins on the board')
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)
GPIO.setup(25, GPIO.IN)

#initialzation
print('Initializing the variables to zero')
count = 0		#number of pings
start1 = 0		#start time for sensor 1
start2 = 0		#start time for sensor 2
end1 = 0		#end time for sensor 1
end2 = 0		#end time for sensor 2
elapsed1 = 0		#total time sensor 1 started for execution
elapsed2 = 0		#total time sensor 2 started for execution
peoplecount = 0		#number of people
peoplein = 0
hit1 = 0		#sensor 1 detection
hit2 = 0		#sensor 2 detection

#the current date and time 
timestamp = datetime.datetime.now()

#setting up the detection of the sensor, sensor is set to retriggering mode
GPIO.add_event_detect(4, GPIO.FALLING)
GPIO.add_event_detect(25, GPIO.FALLING)

#opening the text file for a "hard copy" on litpi
data = open("/home/pi/People_Count/data.txt", 'a') #'a' means append, 'w' means write which will rewrite entire file

#runnnnnnnnnnnnnnning the program continously until keyboard interrupt (ctrl + C)
while(1):
	#ping means the sensor detected infrared, two sensors, 4 and 25 are GPIO pins on jiglive
        ping1 = GPIO.event_detected(4)
        ping2 = GPIO.event_detected(25)

	#ping = detection, value = 0 (no detection or 1 (detection))
        if (ping1):
                print('Sensor 1 has something')

                if (start1 == 0):			#see end of code of methodology of if statements
                        hit1 = 1

                if (hit1 == 1 and start1 == 0):
                        start1 = time.time()
                        print('Time 1 = ', start1)

        if (ping2):
                print('Sensor 2 has something')

                if (start2 == 0):
                        hit2 = 1

                if (hit2 == 1 and start2 == 0):
                        start2 = time.time()
                        print('Time 2 = ', start2)

        end1 = time.time()		#end time for sensor 1
        end2 = time.time()		#end time for sensor 2

        elapsed1 = end1 - start1	#time elapsed for computation for sensor 1
        elapsed2 = end2 - start2	#time elapsed for computation for sensor 2

	#sensor 1 was pinged first then sensor 2 so someone entered
        if (hit1 == 1 and hit2 == 1 and elapsed1 > elapsed2):
                peoplecount += 1		#increment number of people by 1
		peoplein += 1			#increment number of people that entered by 1
		stringer = str(peoplecount)	#stringer is string variable of peoplecount
		stringpeepsin = str(peoplein)	#stringpeepsin is string variable of peoplein
		stringerdate = str(timestamp)	#stringerdate is string variable of timestamp
		#the strings are necessary to write to the text file data.txt
               
		print('Someone entered this joint little daddy')
                print('Total Personel = ', peoplecount)

		#writing to data.txt
		data.write("People in this joint ")
		data.write(stringer)
		data.write("  at ")
                data.write(stringerdate)
		data.write("\n")

		#outputing the count to the Litpeople table in the database, also must be in string format, must commit
		cursor.execute("INSERT INTO Litpeople VALUES (%s,%s)", (stringerdate, stringer))
		database.commit()

		#outputing the running count into total table in the database, must be in string format, must commit
		cursor.execute("INSERT INTO total VALUES (%s,%s)", (stringpeepsin, stringerdate))
		database.commit()

		#reset the variables to 0 for recomputuation
                hit1 = 0
                hit2 = 0
                start1 = 0
                start2 = 0
                end1 = 0
                end2 = 0
                elapsed1 = 0
                elapsed2 = 0

	#sensor 2 pinged first then sensor 1, someone exited
        if (hit1 == 1 and hit2 == 1 and elapsed2 > elapsed1):
                peoplecount -= 1	 #decrement the number of people by 1
		stringer = str(peoplecount)
		stringerdate = str(datetime)
               
		print('Someone left this joint little daddy')
                print('Total Personel = ', peoplecount)

		data.write("People in this joint ")
		data.write(stringer)
		data.write("  at ")
                data.write(stringerdate)
		data.write("\n")

		cursor.execute("INSERT INTO Litpeople VALUES (%s,%s)", (stringerdate, stringer))
		database.commit()

		hit1 = 0
                hit2 = 0
                start1 = 0
                start2 = 0
                end1 = 0
                end2 = 0
                elapsed1 = 0
                elapsed2 = 0

	#just needed to know where code execution cursor was
        print('Pausing at End of Code')
        time.sleep(0.5)	#pause execution

#if statements for  start and hit
#start1/2 are beginning times for pings
#hit means there's a detection, but there doesn't need to be another $
# $ detection if a ping is already set to value 1
#so if start time for sensor 1 is 0 then hit 1 is set to 1 for a detection and same $
# $ for sensor 2
#if no detection for either and there is a ping then start time will be given $
# $ time.time(), time.time() = seconds elapsed for code execution at that calling
