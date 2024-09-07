import logging
import mysql.connector
import mysql.connector.pooling
from dotenv import load_dotenv
import os

load_dotenv()

try:
    dbconfig = {
        'host': os.getenv('DBHOST'),
        'user': os.getenv('DBUSER'),
        'password': os.getenv('DBPASSWORD'),
    }
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(
      pool_name='mypool',
      pool_size=3,
      **dbconfig
    )
    cnx1 = cnxpool.get_connection()
except:
    logging.warning('database connection fail')

mycursor = cnx1.cursor()

mycursor.execute('CREATE DATABASE manageall_database')

mycursor.close()

cnx1.close()