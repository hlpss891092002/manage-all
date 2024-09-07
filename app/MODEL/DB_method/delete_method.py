import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime
from dotenv import load_dotenv
from fastapi import  HTTPException
from app.MODEL.data_class.response_class import databaseException

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

def delete_data(condition, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    print(condition)
    delete_index_column= list(condition.keys())[0]
    print(delete_index_column)
    values = condition[delete_index_column]
    print(values)
    try:
        val = list(values)
        sql = f"""DELETE FROM  {table_name} """
        sql_condition = ""
        if len(val) > 1 :
            sql_condition = f"""WHERE {table_name}.{delete_index_column} in ("""
            valNum = len(val)
            count = 0
            while  count < valNum:
                if count == 0 :
                    sql_condition = sql_condition + " %s"
                elif count == len(val)-1:
                    sql_condition = sql_condition + ", %s)"
                else:
                    sql_condition = sql_condition + ", %s "
                count +=1
        else:
            sql_condition = f"""WHERE {table_name}.{delete_index_column}  = %s"""
        sql = sql + sql_condition
        cursor.execute(sql,val)
        con.commit()
        if cursor.rowcount > 0 :
            print(f"delete  category {cursor.rowcount} ")
            return 
        else :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the delete, please check input value")
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

