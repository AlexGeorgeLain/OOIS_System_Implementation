import sqlite3

con = sqlite3.connect('database.db')

#config file to set the sqlite database connection across all modules.
#test.py sets the connection to ":memory:" to connect to a fresh in memory database each time it is run.
