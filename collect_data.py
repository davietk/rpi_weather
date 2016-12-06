#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import random
import os
import glob

from influxdb import client as influxdb

# Pilotes pour le bus 1-wire
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sonde DS18B20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Interval de capture
capture_interval = 10.0 

# Fonction lecture fichier de sortie du capteur
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Fonction qui retourne la temperature en celcius
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# InfluxDB instance
db = influxdb.InfluxDBClient('192.168.99.100', 8086, 'influx', 'influx', 'weather')

try:	
	# Read, Report, Repeat
	while True:

		#temp = random.randint(0,35)
		temp = read_temp()
		now = datetime.datetime.today()
		# influxClient.write_points(temperature_data(temp))
		data = [
		{
		  "measurement": "temperature.readings",
		  "tags": {
			"device": "rpi01",
		  },
		  "fields": {
			"value": int(temp)
		  }
		}
		]
		db.write_points(data)
		print ("Temperature : "+format(temp)+"°C")
		time.sleep(capture_interval)
		
except KeyboardInterrupt:
	sys.exit(0)
