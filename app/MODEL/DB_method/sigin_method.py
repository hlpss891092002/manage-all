import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

#create connection pool
try:
    dbconfig = {
        'host': os.getenv('DBHOST'),
        'user': os.getenv('DBUSER'),
        'password': os.getenv('DBPASSWORD'),
        'database':'manageall_database',
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='mypool',
        pool_size=5,
        **dbconfig
    )
    
except Exception as e:
    print(f'database connection fail {e}')

def check_user(account, password):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    print(account)
    try: 
      sql = """ SELECT account, name FROM staff 
      where account = %s and password = %s"""
      val = (account, password)
      cursor.execute(sql,val)
      result = cursor.fetchone()
      return (result)
    except Exception as e:
        pass
    finally:
      cursor.close()
      con.close()


def get_user_data(account, password):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try: 
      sql = """ SELECT staff.account, staff.name, staff.email, staff.cellphone, authorization.authorization, authorization.job_position FROM staff
        INNER JOIN authorization
        ON staff.authorization_id = authorization.id
        WHERE staff.id = %s AND staff.password = %s
      """
      val = (account, password)
      cursor.execute(sql,val)
      result = cursor.fetchone()
      print(result)
      return (result)
    except Exception as e:
        pass
    finally:
      con.close()
      cursor.close()