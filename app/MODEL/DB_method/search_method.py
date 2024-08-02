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
            column["Field"] = column["Field"].replace("_id", "")
            columns_list.append(column["Field"])
        return(columns_list)
        # print(f"get media list")
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()


def get_variety_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select variety.id, variety.variety_code, variety.description, category.category
        FROM variety 
        INNER JOIN  category
        WHERE variety.category_id = category.id;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        variety_list = []
        for variety in result:
            variety_list.append(variety)
        return(variety_list)
        # print(f"get media list")
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_media_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select id, media_name from media;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_stage_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select id, stage_name from stage;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_category_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select id, category from category;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_client_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select id, name, description from client;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_client_order_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT * FROM  client_order  
        inner join client 
        on  client_order.client_id =  client.id inner 
        join  variety 
        on client_order.variety_id = variety.id 
;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        print (result)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_staff_data():
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT staff.id, staff.name, staff.account authorization.job_position authorization.authorization FROM  staff 
        INNER JOIN authorization 
        ON staff.authorization_id = authorization.id;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_produce_record_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT produce_record.id,  variety.variety_code, variety.name as variety, media.media_name as media, staff.name as producer, staff.account as producer_id, stage.stage_name as stage, DATE_FORMAT(produce_record.manufacturing_date, "%Y/%m/%d")  as test
        FROM  produce_record 
        INNER JOIN  variety
        ON  produce_record.variety_id = variety.id
        INNER JOIN  media
        ON  produce_record.media_id = media.id
        INNER JOIN  staff
        ON  produce_record.producer_id = staff.id
        INNER JOIN  stage
        ON  produce_record.stage_id = stage.id
        """

        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            print(condition)
            columns = list(condition.keys())
            print(columns)
            for column in columns:
                if columns.index(column) == 0 :
                    condition_individual=f"""produce_record.{column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                    
                else:
                    condition_individual=f""" AND produce_record.{column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            print(sql)
            print(val)
            cursor.execute(sql,val)
        else:
            cursor.execute(sql)
        
        result = cursor.fetchall()
        print (result)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()
 