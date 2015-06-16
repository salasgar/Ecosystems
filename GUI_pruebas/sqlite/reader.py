import sqlite3
import matplotlib.pyplot
from time import sleep
conn = sqlite3.connect('example.db', isolation_level=None)

c = conn.cursor()
while True:
    c.execute("SELECT * FROM statistics")
    try:
	print '---'
        print c.fetchall()
    except:
        pass
    sleep(3)
