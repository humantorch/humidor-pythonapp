#!/usr/bin/python
import MySQLdb
import time
from random import randint
import config #config file containing db connection info

# create a separate 'config.py' file and put the following into it (with your own values, obv)
# pro tip: put config.py and *.pyc in your .gitignore file


    # user = "username"
    # db = "database name"
    # pword = "database password"
    # host = "localhost"


db = MySQLdb.connect(host=config.host,
                     user=config.user,
                     passwd=config.pword,
                     db=config.db)

cur = db.cursor()
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')

#temporary random number generation until device setup
humid = randint(60,75)
temp = randint(60,75)

try:
	cur.execute("INSERT INTO data(curdate, humidity, temperature) VALUES (%s, %s, %s)",(nowtime, humid, temp))
	db.commit()

except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)

db.close()
