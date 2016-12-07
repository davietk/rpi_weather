#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import random
import RPi.GPIO as GPIO
import dht11
import sys

#from influxdb import client as influxdb

# Interval de capture
capture_interval = 10.0

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Read data using pin 4
instance = dht11.DHT11(pin=4)

# InfluxDB instance
db = influxdb.InfluxDBClient('192.168.0.78', 8086, 'influx', 'influx', 'weather')

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

    # Recuperation data sonde
    result = instance.read()

    if result.is_valid():

      # Temperature
      temperature = result.temperature
      # Humidity
      humidity = result.humidity
      # Date
      now = datetime.datetime.today()

      data = [
      {
        "measurement": "temperature.readings",
        "tags": {
        "device": "rpi01",
        },
        "fields": {
        "value": int(temperature)
        }
      }
      ]
      db.write_points(data)

      print ("---------------------")
      print (dateClock())
      print ("---------------------")
      print("Temperature: %d°C" % result.temperature)
      print("Humidity: %d %%" % result.humidity)
      print ("=====================\n")

    time.sleep(capture_interval)
    
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
  sys.exit(0)
