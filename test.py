import config
#import config module for database connection
import sqlite3
#sqlite for altering database connection

config.con = sqlite3.connect(":memory:")  # alters config variable to connect to in-memory database for testing

import test_database
test_database.build_db()  # build in-memory database with test data

import interface
interface.start()  # import interface and begin command line interface
