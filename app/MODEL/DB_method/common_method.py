import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from fastapi import  HTTPException

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

def get_table_columns(table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql=f"""SHOW COLUMNS FROM {table_name};
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        columns_list = []
        for column in result:
            columnName = column["Field"]
            if columnName == "mother_produce_id" or columnName == "employee_id" :
                columns_list.append(columnName)
                continue
            elif columnName == "variety_id":
                columnName = columnName.replace("_id", "_code")
                columns_list.append(columnName)
                continue
            columnName = column["Field"].replace("_id", "")
            columns_list.append(columnName)
        return(columns_list)
        # print(f"get media list")
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_yesterday_produce_most():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        yesterday = now - timedelta(days=1)
        print(yesterday)
        sql="""SELECT variety_code, stage.name as stage, count(produce_record.id) as count
        FROM produce_record        
        inner JOIN variety
        ON produce_record.variety_id = variety.id 
        INNER JOIN stage
        ON produce_record.stage_id = stage.id 
        where produce_date = %s  and in_stock = 1
        group by variety_code, stage.name
        
        """
        val = list()
        val.append(yesterday)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        # print(result)
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_yesterday_consume_by_category():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        yesterday = now - timedelta(days=1)
        print(yesterday)
        sql="""SELECT variety_code, stage.name as stage, count(produce_record.id) as count
        FROM produce_record
        INNER JOIN stage
        ON produce_record.stage_id = stage.id        
        inner JOIN variety
        ON produce_record.variety_id = variety.id 
        where produce_date = %s  and in_stock = 0
        group by variety_code, stage.name
        ;
        """
        val = list()
        val.append(yesterday)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_category_stock():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        yesterday = now - timedelta(days=1)
        print(yesterday)
        sql="""SELECT category.name as category,  count(produce_record.id) as count 
        FROM produce_record
        inner JOIN variety
        ON produce_record.variety_id = variety.id  
        INNER JOIN category
        ON variety.category_id = category.id
        where in_stock = 1 
        group by category.name 
        ;
        """
        val = list()
        val.append(yesterday)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_ready_stock():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        # shipping_date_diff = now - timedelta(weeks=4)
        sql="""SELECT category.name as category, variety.variety_code as variety_code ,  count(produce_record.id) as count 
        FROM produce_record
        inner JOIN variety
        ON produce_record.variety_id = variety.id
        INNER JOIN category
        ON variety.category_id = category.id 
        where in_stock = 1   and stage_id = 5  and DATEDIFF(%s, produce_date) >= 1
        group by variety_code;
        """
        val = list()
        val.append(now)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()
    
def get_foreign_column(table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql = """
                SELECT     COLUMN_NAME 
                FROM  INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                
                WHERE
                TABLE_NAME = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL
                """
        val = list()
        val.append(table_name)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        column_list = list()
        for column in result:
            column_list.append(column["COLUMN_NAME"])
        return column_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_column_value_distinct(column, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        if column == "mother_produce_id":
            return
        elif column =="employee_id":
            FK_table = "staff"
        else:
            FK_table = column.replace("_id", "")
    
        if FK_table == "variety":
            FK_column = "variety_code"
        elif FK_table == "staff":
            FK_column = column
        else:
            FK_column = "name"
        
        sql = f"""
                SELECT  DISTINCT {FK_table}.{FK_column} FROM {table_name}
                INNER JOIN {FK_table}
                ON {table_name}.{column} = {FK_table}.id
                """     
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        value_list= list()
        for key_pair in result:
            value = list(key_pair.values())[0]
            value_list.append(value)
        return value_list

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()