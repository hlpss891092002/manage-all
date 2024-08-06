import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime
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

def get_category_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select category, description from category
        """
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            print(condition)
            print(sql)
            columns = list(condition.keys())
            print(columns)
            for column in columns:
                if columns.index(column) == 0 :
                    condition_individual=f""" {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                else:
                    condition_individual=f""" AND {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            
            cursor.execute(sql,val)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        else:
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_client_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select name, description from client
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
                    condition_individual=f""" {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                else:
                    condition_individual=f""" AND {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            cursor.execute(sql,val)
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        else:
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_media_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select name, description from media
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
                    condition_individual=f""" {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                else:
                    condition_individual=f""" AND {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            cursor.execute(sql,val)
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        else:
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_stage_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select name, description from stage
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
                    condition_individual=f""" {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                else:
                    condition_individual=f""" AND {column} = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            cursor.execute(sql,val)
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()


def get_produce_record_data_from_condition(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT produce_record.id,  variety.variety_code, variety.name as variety, media.name as media, staff.name as producer, staff.account as producer_id, stage.name as stage, DATE_FORMAT(produce_record.manufacturing_date, "%Y/%m/%d")  as date, produce_record.mother_produce_id, produce_record.in_stock, produce_record.consumed_reason
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
            # print(condition)
            columns = list(condition.keys())
            print(columns)
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "id" or column == "manufacturing_date" or column == "mother_produce_id" or column == "consumed_reason" :
                        condition_individual=f""" produce_record.{column} = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                    elif column == "producer_id":
                        condition_individual=f""" staff.account = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                    elif column == "variety_code":
                        condition_individual=f""" variety.variety_code = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                    else:
                        condition_individual=f""" {column}.name = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                else:
                    if column == "id" or column == "manufacturing_date" or column == "mother_produce" or column == "consumed_reason"  :
                        condition_individual=f""" AND produce_record.{column} = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                    elif column == "producer":
                        condition_individual=f""" AND staff.name = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual
                    else:
                        condition_individual=f""" AND {column}.name = %s"""
                        val.append(condition[f"{column}"])
                        sql = sql  + condition_individual

            # print(val)
            cursor.execute(sql,val)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        else:   
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_current_stock(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT produce_record_id FROM  current_stock
        where produce_record_id = %s
        """
        val = (condition,)
        cursor.execute(sql,val)
        result = cursor.fetchall()
        print(result)
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()