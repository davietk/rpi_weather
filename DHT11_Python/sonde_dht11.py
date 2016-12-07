#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import dht11
import time
import datetime

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Read data using pin 4
instance = dht11.DHT11(pin=4)

# Interval de capture
capture_interval = 10.0 

# result = instance.read()
# print '==============='
# print result.temperature
# print '==============='
# print result.humidity
# print '==============='

# Horloge
def dateClock():
    now = datetime.datetime.now()
    day = str(now.day).zfill(2)
    month = str(now.month).zfill(2)
    year = str(now.year)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    second = str(now.second).zfill(2)

    return day+'/'+month+'/'+year+' '+hour+':'+minute+':'+second

# Catch when script is interrupted, cleanup correctly
try:
	# Main loop
	while True:
		# Recuperation data
		result = instance.read()

		if result.is_valid():

			# print("Last valid input: " + str(datetime.datetime.now()))
			# print("Temperature: %d C" % result.temperature)
			# print("Humidity: %d %%" % result.humidity)

			print ("---------------------")
			print (dateClock())
			#print("Last valid input: " + str(datetime.datetime.now()))
			print ("---------------------")
			print("Temperature: %d°C" % result.temperature)
			print("Humidity: %d %%" % result.humidity)
			print ("=====================\n")
			#print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(result.temperature, result.humidity))
		# 
		time.sleep(capture_interval)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()