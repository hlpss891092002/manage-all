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
        pool_size=10,
        **dbconfig
    )
    # print('database connected')
except mysql.connector.Error as e:
    print(f'database connection fail {e}')

con = connection_pool.get_connection()
cursor = con.cursor(dictionary = True, buffered = True)
sql_index_category_category = """CREATE INDEX idx_category_category ON category (name);"""
sql_index_client_name = """CREATE INDEX idx_client_name ON client (name);"""
# sql_index_client_order_id = """CREATE INDEX idx_client_order_id ON client_order (client_id);"""
sql_index_media_name = """CREATE INDEX idx_media_name ON media (name);"""

sql_index_staff_name = """CREATE INDEX idx_staff_employee_id ON staff (employee_id);"""
sql_index_stage_name = """CREATE INDEX idx_stage_name ON stage (name);"""
sql_index_variety_variety_code = """CREATE INDEX idx_variety_variety_code ON variety  (variety_code);"""
sql_index_variety_category_id  = """CREATE INDEX idx_variety_category_id ON variety  (category_id);"""

sql_index_produce_record_for_count = """-- CREATE INDEX idx_produce_record_count_2 
--     ON produce_record(variety_id, media_id, employee_id, stage_id, produce_date, in_stock, consumed_reason);"""

cursor.execute(sql_index_category_category)
cursor.execute(sql_index_client_name)
cursor.execute(sql_index_media_name)
cursor.execute(sql_index_staff_name)
cursor.execute(sql_index_stage_name)
cursor.execute(sql_index_variety_variety_code)
cursor.execute(sql_index_variety_category_id)
cursor.execute(sql_index_produce_record_for_count)


# sql_index_produce_record_foreign_key_variety = """
# CREATE INDEX idx_produce_record_variety_code ON produce_record  (variety_id);
# """
# sql_index_produce_record_id_foreign_key_variety = """
# CREATE INDEX idx_produce_record_id_and_variety_code ON produce_record  (id, variety_id);
# """

# sql_index_produce_record_foreign_key ="""

# CREATE INDEX idx_produce_record_employee_id ON produce_record  (employee_id);
# CREATE INDEX idx_produce_record_variety_id ON produce_record  (variety_id);"""

show_index = "show index from produce_record"
drop_index = "drop index idx_produce_record_stage on produce_record"

sql_count = f"""explain analyze Select count(produce_record.id) from produce_record 
             JOIN  variety
            ON  produce_record.variety_id = variety.id
             JOIN  media
            ON  produce_record.media_id = media.id
             JOIN  staff
            ON  produce_record.employee_id = staff.id
             JOIN  stage
            ON  produce_record.stage_id = stage.id
            limit 10000
            """

# cursor.execute(sql_index_produce_record_id_in_stocK_foreign_key_variety)


# cursor.execute(show_index)
result = cursor.fetchall()
# for index in result:
#     print(index["Key_name"], " : ", index["Column_name"])
print(result)
cursor.close()
con.close()