#pulling all the necessary libraries
import RPi.GPIO as GPIO
import time
import datetime
#import sqlite3#### not being used###
import urllib2
import subprocess
import MySQLdb

#making sure there is wifi, if no wifi then run script forcewifi to get wifi LOOOOL
print('Can you connect to the world wide web?')
def internet_on():
	try:
		urllib2.urlopen('https://www.google.com', timeout = 1)
		print ('Connected')
		return True

	except urllib2.URLError as err:
		print ('Not connected')
		return False

#print internet_on()

tries = 0
while (internet_on() == False):
	tries += 1

	if (tries < 4):
		print ('This is try number: ', tries)

	if (tries > 3):
		print ('You tried three times to connect')
		print ('Having some connection issues')
		print ('Leaving the loop now...')
		break
	
	print ('Running "getthewifi" scirpt')
	subprocess.call('/home/pi/People_Count/getthewifi.sh')

	print ('Now about to about to pull up google.com')
#	if (urllib2.urlopen('https://www.google.com', timeout = 1)):
#		print ('It worked')
#		print ('Now you are connected')
#		break

	print ('Are you connected?')

	internet_on()

	if (internet_on() == True):
		print ('You are now connected')
		print ('Continue to code execution')
		break

	print ('No dice, trying again.....')

#connection = urllib2.Request('https://www.google.com')
#wifi = 0

#try: urllib2.urlopen(connection)
#except URLError as err:
#	wifi = 1

#while(wifi == 1):
#	subprocess.call(['/home/pi/People_Count/forcewifi.sh'])

#	try: urllib2.urlopen(connection)#################need to finish
############################################################################################################################################################
	
#connecting to the database on phpmyadmin, setting up cursor for outputing to database
database = MySQLdb.connect(user = 'root', passwd = 'scottyfresh', db = 'people', host = 'localhost', port = 3306)
cursor = database.cursor()

#not used#####################################
#conn = sqlite3.connect('people.db')
#cursor = conn.cursor()
##############################################

#setting up the pins on the litpi for power, ground and data
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)
GPIO.setup(25, GPIO.IN)

#initialzation
count = 0		#number of pings
start1 = 0		#start time for sensor 1
start2 = 0		#start time for sensor 2
end1 = 0		#end time for sensor 1
end2 = 0		#end time for sensor 2
elapsed1 = 0		#total time sensor 1 started for execution
elapsed2 = 0		#total time sensor 2 started for execution
#first1 = 0		#sensor 1 determination, first, value = 0 or 1 #not being used#################
#first2 = 0		#sensor 2 determination, first, value = 0 or 1 #not being used ################
#second1 = 0		#sensor 1 determination, second, value = 0 or 1 #not being used ###############
#second2 = 0		#sensor 2 determination, second, value = 0 or 1 #not being used ###############
peoplecount = 0		#number of people
peepsin = 0		#number of people that enter only
hit1 = 0		#sensor 1 detection
hit2 = 0		#sensor 2 detection

#the current date and time 
timestamp = datetime.datetime.now()

#setting up the detection of the sensor, sensor is set to retriggering mode
GPIO.add_event_detect(4, GPIO.RISING)
GPIO.add_event_detect(25, GPIO.RISING)

#opening the text file for a "hard copy" on litpi
data = open("/home/pi/People_Count/data.txt", 'a') #'a' means append, 'w' means write which will rewrite entire file

#runnnnnnnnnnnnnnning the program continously until keyboard interrupt (ctrl + C)
while(1):
	#ping means the sensor detected infrared, two sensors, 5 and 25 are GPIO pins on litpi
        ping1 = GPIO.event_detected(4)
        ping2 = GPIO.event_detected(25)

#not being used ###############################################
#        if (elapsed1 > 3):
 #               start1 = 0
  #              hit1 = 0
   #             count = 0

    #    if (elapsed2 > 3):
     #           start2 = 0
      #          hit2 = 0
       #         count = 0

#       if (count == 2):
#               start1 = 0
#               start2 = 0
#               first1 = 0
#               first2 = 0
#               second1 = 0
####################################################################

	#ping = detection, value = 0 (no detection or 1 (detection)
        if (ping1):
#                if (count == 0): # not in use########################
#                       count += 1 # not in use#######################

                print('Sensor 1 has something')

#not in use##########################################################
#               print('Count = ', count)
#               start1 = time.time()
#               print('Time 1 = ', start1)
#####################################################################

                if (start1 == 0):			#see end of code of methodology of if statements
                        hit1 = 1

                if (hit1 == 1 and start1 == 0):
                        start1 = time.time()
                        print('Time 1 = ', start1)

#not in use ##################################################################
#               if (start2 == 0):
#                       first1 = 1
#                       first2 = 0
                #       second1 = 0
                #       second2 = 1

#               if (first2 == 1):
#                       first1 = 0
#               #       second1 = 1

        #       count += 1
#               print('Pausing for Sensor 1')
        #       time.sleep(0.5)
#################################################################################

        if (ping2):
                print('Sensor 2 has something')

#not in use###################################################
#               print('Count = ', count)
#               start2 = time.time()
#               print('Time 2 = ', start2)
###################################################################

                if (start2 == 0):
                        hit2 = 1

                if (hit2 == 1 and start2 == 0):
                        start2 = time.time()
                        print('Time 2 = ', start2)

#not in use ########################################################
#               if (start1 == 0):
                #       first1 = 0
                #       first2 = 1
#                       second1 = 1
#                       second2 = 0

#               if (first1 == 1):
                #       first2 = 0
#                       second2 = 1

        #       count += 1
#               print('Pausing for Sensor 2')
        #       time.sleep(0.5)
#####################################################################

        end1 = time.time()		#end time for sensor 1
        end2 = time.time()		#end time for sensor 2

        elapsed1 = end1 - start1	#time elapsed for computation for sensor 1
        elapsed2 = end2 - start2	#time elapsed for computation for sensor 2

#not in use##################################################################################
#       if (count == 2 and first1 == 1 and second2 == 1):
#               peoplecount += 1
#               print('Someone entered this joint cuz')
#               print('Total Personel is ', peoplecount)

#       if (count == 2 and first2 == 1 and second1 == 1):
#               peoplecount -= 1
#               print('Someone left this joint cuz')
#               print('Total Personel is ', peoplecount)
#not in use####################################################################################

	#sensor 1 was pinged first then sensor 2 so someone entered
        if (hit1 == 1 and hit2 == 1 and elapsed1 > elapsed2):
                peoplecount += 1		#increment number of people by 1
		peepsin += 1			#increment number of people that entered by 1
		stringer = str(peoplecount)	#stringer is string variable of peoplecount
		stringerdate = str(timestamp)	#stringerdate is string variable of timestamp
		#the strings are necessary to write to the text file data.txt and entering to database
		strpeeps = str(peepsin)		#string value for peepsin
               
		print('Someone entered this joint little daddy')
                print('Total Personel = ', peoplecount)

		#writing to data.txt
		data.write("People in this joint ")
		data.write(stringer)
		data.write("  at ")
                data.write(stringerdate)
		data.write("\n")

#not in use##########################################################################################
#		lit = "INSERT INTO Litpeople(when, count) VALUES (%s,%s)"
#		litstring = str(lit)
#		cursor.execute(litstring,(stringerdate, stringer))
#####################################################################################################

		#outputing the count to the table in the database, also must be in string format, must commit
		cursor.execute("INSERT INTO Litpeople VALUES (%s,%s)", (stringerdate, stringer))
		database.commit()

		cursor.execute("INSERT INTO total VALUES (%s)", (strpeeps))
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
                peoplecount -= 1 #decrement the number of people by 1
		stringer = str(peoplecount)
		stringerdate = str(time)
               
		print('Someone left this joint little daddy')
                print('Total Personel = ', peoplecount)

		data.write("People in this joint ")
		data.write(stringer)
		data.write("  at ")
                data.write(stringerdate)
		data.write("\n")

		lit = "INSERT INTO Litpeople (when, count) VALUES (%s,%s)"
		litstring = str(lit)

################cursor.execute(litstring, (stringerdate, peoplecount)) # not being used###############################

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
        time.sleep(0.5)

#       GPIO.cleanup() # not necessary####################################

#if statements for  start and hit
#start1/2 are beginning times for pings
#hit means there's a detection, but there doesn't need to be another $
#$detection if a ping is already set to value 1
#so if start time for sensor 1 is 0 then hit 1 is set to 1 for a detection and same $
#$for sensor 2
#if no detection for either and there is a ping then start time will be given $
#$time.time(), time.time() = seconds elapsed for code execution at that calling
