#!/usr/bin/python
import MySQLdb
import time
import random
import decimal
import config

#print config.pword

db = MySQLdb.connect(host=config.host,
                     user=config.user,
                     passwd=config.pword,
                     db=config.db)

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')

#temporary random number generation until device setup
humid = round(random.uniform(60,75), 1)
temp = round(random.uniform(60,75), 1)

# Use all the SQL you like
try:
	cur.execute("INSERT INTO data(curdate, humidity, temperature) VALUES (%s, %s, %s)",(nowtime, humid, temp))
	db.commit()
	# cur.execute("SELECT * FROM data")
except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)

# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

db.close()
