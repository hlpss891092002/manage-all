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
        'database':'manageall_database',
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='mypool',
        pool_size=5,
        **dbconfig
    )
    # print('database connected')
except mysql.connector.Error as e:
    print(f'database connection fail {e}')

con = connection_pool.get_connection()
cursor = con.cursor(dictionary = True, buffered = True)
sql_index_category_category = """CREATE INDEX category_category ON category (category);"""
sql_index_client_name = """CREATE INDEX client_name ON client (name);"""
sql_index_client_order_id = """CREATE INDEX client_order_id ON client_order (id);"""
sql_index_media_name = """CREATE INDEX media_name ON media (name);"""
sql_index_produce_record_id = """CREATE INDEX produce_record_id ON produce_record  (id);"""
sql_index_staff_name = """CREATE INDEX staff_name ON staff (name);"""
sql_index_stage_name = """CREATE INDEX stage_name ON stage (name);"""
sql_index_variety_variety_code = """CREATE INDEX variety_variety_code ON variety 
 (variety_code);"""
cursor.execute(sql_index_category_category)
cursor.execute(sql_index_client_name)
cursor.execute(sql_index_client_order_id)
cursor.execute(sql_index_media_name)
cursor.execute(sql_index_produce_record_id)
cursor.execute(sql_index_staff_name)
cursor.execute(sql_index_variety_variety_code)
cursor.execute(sql_index_stage_name)

cursor.close()
con.close()