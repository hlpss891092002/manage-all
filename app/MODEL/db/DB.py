import mysql.connector
import mysql.connector.pooling
import os
from dotenv import load_dotenv


load_dotenv()


class DB:
  def __init__(self, database):
    self.database = database
    self.cnx_pool = None
  
  def initialize(self):
    dbconfig = {
      "host": os.getenv("DBHOST"),
      "user": os.getenv("DBUSER"),
      "password": os.getenv("DBPASSWORD"),
      "database": self.database
    }
    self.cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **dbconfig
    )