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
# sql_index_category_category = """CREATE INDEX idx_category_category ON category (category);"""
# sql_index_client_name = """CREATE INDEX idx_client_name ON client (name);"""
# sql_index_client_order_id = """CREATE INDEX idx_client_order_id ON client_order (id);"""
# sql_index_media_name = """CREATE INDEX idx_media_name ON media (name);"""
# sql_index_produce_record_id = """CREATE INDEX idx_produce_record_id ON produce_record  (id);"""
# sql_index_staff_name = """CREATE INDEX idx_staff_name ON staff (name);"""
# sql_index_stage_name = """CREATE INDEX idx_stage_name ON stage (name);"""
# sql_index_variety_variety_code = """CREATE INDEX idx_variety_variety_code ON variety  (variety_code);"""
# sql_index_produce_record_foreign_key ="""
# CREATE INDEX idx_produce_record_variety_id ON produce_record(variety_id);
# CREATE INDEX idx_produce_record_media_id ON produce_record(media_id);
# CREATE INDEX idx_produce_record_producer_id ON produce_record(producer_id);
# CREATE INDEX idx_produce_record_stage_id ON produce_record(stage_id);
# """

sql_drop_index_category_category = """DROP INDEX category_category ON category (category);"""
sql_drop_index_client_name = """DROP INDEX client_name ON client (name);"""
sql_drop_index_client_order_id = """drop INDEX client_order_id ON client_order (id);"""
sql_drop_index_media_name = """DROP INDEX media_name ON media (name);"""
sql_drop_index_produce_record_id = """DROP INDEX produce_record_id ON produce_record  (id);"""
sql_drop_index_staff_name = """DROP INDEX staff_name ON staff (name);"""
sql_drop_index_stage_name = """DROP INDEX stage_name ON stage (name);"""
sql_drop_index_variety_variety_code = """DROP INDEX variety_variety_code ON variety  (variety_code);"""


# cursor.execute(sql_index_category_category)
# cursor.execute(sql_index_client_name)
# cursor.execute(sql_index_client_order_id)
# cursor.execute(sql_index_media_name)
# cursor.execute(sql_index_produce_record_id)
# cursor.execute(sql_index_staff_name)
# cursor.execute(sql_index_variety_variety_code)
# cursor.execute(sql_index_stage_name)

cursor.execute(sql_drop_index_category_category)
cursor.execute(sql_drop_index_client_name)
cursor.execute(sql_drop_index_client_order_id)
cursor.execute(sql_drop_index_media_name)
cursor.execute(sql_drop_index_produce_record_id)
cursor.execute(sql_drop_index_staff_name)
cursor.execute(sql_drop_index_stage_name)
cursor.execute(sql_drop_index_variety_variety_code )

cursor.close()
con.close()