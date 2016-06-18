#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import time
import random
import decimal
import math
import config # get values from config.py
import sys
import Adafruit_DHT # https://github.com/adafruit/Adafruit_Python_DHT
import tweepy # https://github.com/tweepy/tweepy

# Parse command line parameters for sensor reading
# TODO: once the final setup is complete hard-code these values
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22, # this is the one I'm using
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./humidor.py [11|22|2302] GPIOpin#')
    print('example: sudo ./humidor.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)



# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Comment out the line below to convert the temperature to Celsius.
temperature = temperature * 9/5.0 + 32

if humidity is not None and temperature is not None:
    humid = humidity
    temp = temperature
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

# set up db connection (uses values from config.py)
db = MySQLdb.connect(host=config.host,
                     user=config.user,
                     passwd=config.pword,
                     db=config.db)

cur = db.cursor()
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')

try:
	# push info to database
	cur.execute("INSERT INTO data(curdate, humidity, temperature) VALUES (%s, %s, %s)",(nowtime, humid, temp))
	db.commit()

	# post to Twitter (uses values from config.py)
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_secret)
	api = tweepy.API(auth)
    # TODO: detect if temp/humidity values are outside safety range and add an @ notification to my main Twitter account if so
	status = "Humidity: "+str(math.floor(humid*10)/10)+"%, Temperature: "+str(math.floor(temp*10)/10)+"ºF, as of: "+str(nowtime)
	api.update_status(status=status)

except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)

db.close()
