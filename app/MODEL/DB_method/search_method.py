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


def get_category_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select category, description from category
        """
        sql_order = "ORDER BY id DESC"
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
                else:
                    condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
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
        sql_order = "ORDER BY id DESC"
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
                else:
                    condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
            print(sql)
            print(val)
        else:
            sql = sql + sql_order
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

def get_client_order_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)

    try:
        sql="""SELECT client_order.id as order_id, client.name as client, variety.variety_code, amount, creation_date, shipping_date FROM  client_order  
        inner join client 
        on  client_order.client_id =  client.id inner 
        join  variety 
        on client_order.variety_id = variety.id 
        """
        sql_order = "ORDER BY client_order.id DESC"
        if condition:
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            columns = list(condition.keys())
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "variety_code":
                        condition_individual=f""" variety.{column} = %s"""
                    elif column == "client":
                        condition_individual=f""" {column}.name = %s"""
                    else:
                        condition_individual=f""" client_order.{column} = %s"""
                else:
                    if column == "variety_code":
                        condition_individual=f""" AND variety.{column} = %s"""
                    elif column == "client":
                        condition_individual=f""" AND {column}.name = %s"""
                    else:
                        condition_individual=f""" AND client_order.{column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
            cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            keys = data.keys()
            for key in keys:
                if "date" in key:
                    data[f"{key}"] = datetime.strftime(data[f"{key}"], "%Y-%m-%d")
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
        sql_order = "ORDER BY id DESC"
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
                else:
                    condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
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
        sql_order = "ORDER BY produce_record.manufacturing_date DESC"
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            # print(condition)
            columns = list(condition.keys())
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "id" or column == "manufacturing_date" or column == "mother_produce_id" or column == "consumed_reason" :
                        condition_individual=f""" produce_record.{column} = %s"""
                    elif column == "producer_id":
                        condition_individual=f""" staff.account = %s"""
                    elif column == "variety_code":
                        condition_individual=f""" variety.variety_code = %s"""
                    elif column == "in_stock":
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        else:
                           condition[f"{column}"] = 0
                        condition_individual=f""" {column} = %s"""
                    else:
                        condition_individual=f""" {column}.name = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
                else:
                    if column == "id" or column == "manufacturing_date" or column == "mother_produce_id" or column == "consumed_reason" :
                        condition_individual=f""" AND produce_record.{column} = %s"""
                    elif column == "producer_id":
                        condition_individual=f""" AND staff.account = %s"""
                    elif column == "variety_code":
                        condition_individual=f""" AND variety.variety_code = %s"""
                    elif column == "in_stock":
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                           condition[f"{column}"] = 0
                        condition_individual=f""" AND produce_record.{column} = %s"""
                    else:
                        condition_individual=f""" AND {column}.name = %s"""
                    val.append(condition[f"{column}"])
                    sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
            cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            keys = data.keys()
            for key in keys:
                if "in_" in key:
                    print(key)
                    if data[f"{key}"] == 0:
                        data[f"{key}"] = "NO"
                    elif data[f"{key}"] == 1:
                        data[f"{key}"] = "YES"
        if(len(result) == 0):
            return None
        else:   
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_staff_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""SELECT staff.account, staff.name, staff.email, staff.cellphone,  staff.in_employment , authorization.job_position  FROM  staff 
        INNER JOIN authorization 
        ON staff.authorization_id = authorization.id
        """
        sql_order = "ORDER BY staff.id DESC"
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            print(condition)
            columns = list(condition.keys())
            print(columns)
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "in_employment":
                        print(column)
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                           condition[f"{column}"] = 0
                        condition_individual=f""" {column} = %s"""
                    else:
                        condition_individual=f""" {column} = %s"""
                else:
                    if column == "in_employment":
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                           condition[f"{column}"] = 0
                        condition_individual=f""" AND {column} = %s"""
                    else:
                        condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
            cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            keys = data.keys()
            for key in keys:
                if "in_" in key:
                    print(key)
                    if data[f"{key}"] == 0:
                        data[f"{key}"] = "NO"
                    elif data[f"{key}"] == 1:
                        data[f"{key}"] = "YES"
        if(len(result) == 0):
            return None
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
        sql_order = "ORDER BY stage.id DESC"
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
                else:
                    condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
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

def get_variety_data(condition):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql="""Select variety.variety_code, variety.name, variety.description, category.category
        FROM variety 
        INNER JOIN  category
        ON variety.category_id = category.id
        """
        sql_order = "ORDER BY variety.id DESC"
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            val = list()
            print(condition)
            columns = list(condition.keys())
            print(columns)
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "category":
                        condition_individual=f""" category.{column} = %s"""
                    else:
                        condition_individual=f""" variety.{column} = %s"""
                else:
                    if column == "category":
                        condition_individual=f""" AND category.{column} = %s"""
                    else:
                        condition_individual=f""" AND variety.{column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql  + condition_individual
            sql = sql + sql_order
            cursor.execute(sql,val)
        else:
            sql = sql + sql_order
            cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return None
        else:
            return result
    except Exception as e:
        raise e
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
        sql_order = "ORDER BY current_stock.id DESC"
        val = (condition,)
        sql = sql + sql_order
        cursor.execute(sql,val)
        result = cursor.fetchall()
        print(result)
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()