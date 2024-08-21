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
            if columnName == "mother_produce_id" or columnName == "employee_id" or columnName == "producer_id":
                columns_list.append(columnName)
                continue
            elif columnName == "variety_id":
                print(columnName)
                columnName = columnName.replace("_id", "_code")
                columns_list.append(columnName)
                continue
            columnName = column["Field"].replace("_id", "")
            columns_list.append(columnName)
        print(columns_list)
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
        where manufacturing_date = %s  and in_stock = 1
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
        where manufacturing_date = %s  and in_stock = 0
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
        sql="""SELECT category.name as category, stage.name as stage, count(produce_record.id) as count 
        FROM produce_record
        inner JOIN stage
        ON produce_record.stage_id = stage.id 
        inner JOIN variety
        ON produce_record.variety_id = variety.id  
        INNER JOIN category
        ON variety.category_id = category.id
        where in_stock = 1 
        group by category.name, stage.name
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
        where in_stock = 1   and stage_id = 5  and DATEDIFF(%s, manufacturing_date) >= 1
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
    