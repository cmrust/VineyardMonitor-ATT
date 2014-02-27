import serial
import threading
from datetime import datetime
from m2x.client import M2XClient

# instantiate our M2X API client
client = M2XClient(key='#REMOVED#')

# instantiate our serial connection to the Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)

# instantiate our global variables
temp = 0
light = 0
now = datetime.utcnow()

def pollArduino():
	# update these globally
	global temp
	global light
	global now

	# poll time (m2x is only UTC currently)
	now = datetime.utcnow()

	# data from the serial port comes in comma-seperated for:
	#  $temp,$light

	# poll temp/light values (rstrip() removes the \n's)
	values = arduino.readline().rstrip().split(',')

	# if our array is not empty
	if len(values) > 1:
		temp = values[0]
		light = values[1]
	
		# print values to the console
		print "tempF: " + temp
		print "light: " + light
		print

	# clear the serial input buffer
	# this keeps it from building up a backlog and causing delays
	arduino.flushInput()

def pushM2X():
	# iterate through any feeds from blueprints
	for feed in client.feeds.search(type='blueprint'):
		# iterate through steams in feeds
		for stream in feed.streams:
			# upload the current values for each stream
			if stream.name == 'temperature':
				stream.values.add_value(temp, now)
			if stream.name == 'light':
				stream.values.add_value(light, now)


while True:
	pollArduino()

	# m2x calls were proving slow, so we've threaded it here so 
	# that the arduino doesn't get backed up while we're waiting

	# create thread for m2x
	m2x_thread = threading.Thread(target=pushM2X)

	# if thread is still alive, pass
	if m2x_thread.is_alive() is not True:
		m2x_thread.start()
