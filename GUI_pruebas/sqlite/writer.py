import sqlite3
import os
from time import sleep
from random import random

# Remove database if exists
if os.path.exists('example.db'):
    os.remove('example.db')

# Connect with database (example.db, it created the file)
conn = sqlite3.connect('example.db', isolation_level=None)
c = conn.cursor()  # a cursor is used to interact with the database

# Creates a table statistics
c.execute("CREATE TABLE statistics (time real, stat1 real, stat2 real)")

# Start writing!
stat1 = 0
stat2 = 0.0
time = 0
while True:
    time += 1
    stat1 += random() * random()
    stat2 += random() / (random() + 0.1)
    sql_command = ("INSERT INTO statistics VALUES (%d,%f,%f)" %
                   (time, stat1, stat2))
    print sql_command
    c.execute(sql_command)
    sleep(0.1)
