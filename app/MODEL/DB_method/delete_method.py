import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

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

def delete_stock_data(production_id):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""DELETE
        FROM current_stock 
        WHERE produce_record_id = %s;
        """
        val = (production_id, )
        cursor.execute(sql,val)
        con.commit()
        return True
        # print(f"get media list")
    except Exception as e:
        raise(f"error {e} on delete_stock_def")  
    finally:
        cursor.close()
        con.close()

delete_stock_data("000067e8-101a-4962-a10d-f9dc0942ff33442e195e-ab09-46a7-b1a7-8274b1f21017")