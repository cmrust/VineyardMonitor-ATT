import requests, serial, time, re, sqlite3, os

# connect to Arduino over serial
arduino = serial.Serial("/dev/ttyUSB0",9600,timeout = 1)

# initialize global variables
stored_value = ""

# user phone numbers are stored in a sqlite database
# this database can be initialized by sqlite3 on the command line like:
#  $ sqlite3 /tmp/phones.db < schema.sql

# connect to sqlite database
conn = sqlite3.connect("/tmp/phones.db")

# we didn't have a server with public ip to receive trigger updates from m2x
#  and so we're using a web-service here called requestb.in,
#  that provides a human-friendly interface for collecting web requests
#  (and then we scrape them)

while True:
	# poll request bin for updated triggers
	r = requests.post('http://requestb.in/y1oz45y1?inspect', data={"ts":time.time()})

	# scan line-by-line through the response
	for line in r.iter_lines():
		# match the line of json that is printed to the page
		if re.search('body prettyprint">{', line):
			# this is pretty rudimentary, but we're basically just seeing
			# if there is any change to the json between polls
			global stored_value
			# if our stored trigger, matches the new trigger, do nothing
			if stored_value == line:
				print "same value still"
			# else, if our trigger is new
			else:
				# store it
				print "new value: " + line
				stored_value =  line
				
				# tell the arduino the trigger was fired
				arduino.write("L")

				# fetch the phone numbers and email them
				cursor = conn.cursor()
				cursor.execute('select text from entries')
				result = cursor.fetchall()
				for number in result:
					# make system call to our local ssmtp server
					cmd = "ssmtp " + number[0] + "@txt.att.net < message2.txt"
					print cmd
					os.system(cmd)
			# break, because we don't need to continue scanning the file
			break