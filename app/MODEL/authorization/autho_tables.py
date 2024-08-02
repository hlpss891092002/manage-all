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
    # print('database connected')
except Exception as e:
    print(f'database connection fail {e}')

def get_table_list_from_auth(account):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary=True, buffered = True)
    tables = ['staff', 'client', 'client_order', 'media', 'stage', 'variety', 'category', 'produce_record']
    try:
        sql = """SELECT authorization.authorization FROM staff
          INNER JOIN authorization
        ON staff.authorization_id = authorization.id 
        WHERE staff.account = %s
         """
        val = (account,)
        print(account)
        cursor.execute(sql,val)
        result = int(cursor.fetchone()["authorization"])
        print(result)
        if result == 1:
            return tables
        elif result > 1 and result < 2:
            return(tables[3:9]) 
        elif result == 4:
            return tables[7:9]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()

