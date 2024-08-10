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


def update_non_foreign_key_data(condition, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index, update_items = condition.values()
    update_index_column = list(update_index.keys())[0]
    update_index_value = list(update_index.values())[0]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(update_items.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                value = update_items[column]
                sql_SET = sql_SET + f"""  {column} = %s """
                val.append(value)
            else:
                 value = update_items[column]
                 sql_SET = sql_SET + f""" , {column}  = %s """ 
                 val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        cursor.execute(sql,val)
        con.commit()
        if cursor.rowcount > 0 :
            print(f"update  category {cursor.rowcount} ")
            return 
        else :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update, please check input value")
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()


def update_client_order_data(condition, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index, update_items = condition.values()
    update_index_column = list(update_index.keys())[0]
    update_index_value = list(update_index.values())[0]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(update_items.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                if column == "client":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" client_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "client":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , client_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f"""  , {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        print(sql)
        print(val)
        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount > 0 :
            print(f"update  category {cursor.rowcount} ")
            return 
        else :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
    finally:
        cursor.close()
        con.close()

def update_produce_record_data(condition, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index, update_items = condition.values()
    update_index_column = list(update_index.keys())[0]
    update_index_value = list(update_index.values())[0]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(update_items.keys())
        print(len(column_list))
        for column in column_list:
            print(column)
            if column_list.index(column) == 0:
                if column == "media":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" media_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                elif column == "producer_id":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" producer_id = (SELECT id FROM staff WHERE employee_id = %s )"""
                elif column == "stage":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" stage_id = (SELECT id FROM stage WHERE name = %s )"""
                elif column == "in_stock":
                    print(column)
                    value =update_items[column]
                    if value == "YES":
                        value = 1
                    elif value == "NO":
                        value = 0
                    else:
                        return
                    sql_SET = sql_SET + f"""  {column} = %s """
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "media":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , media_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                elif column == "producer_id":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , producer_id = (SELECT id FROM staff WHERE employee_id = %s )"""
                elif column == "stage":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , stage_id = (SELECT id FROM stage WHERE name = %s )"""
                elif column == "in_stock":
                    print(column)
                    value =update_items[column]
                    if value == "YES":
                        value = 1
                    elif value == "NO":
                        value = 0
                    else:
                        return
                    sql_SET = sql_SET + f""" ,  {column} = %s """
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f""" ,  {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        print(sql)
        print(val)
        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount > 0 :
            print(f"update  category {cursor.rowcount} ")
            return 
        else :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
    finally:
        cursor.close()
        con.close()

def update_variety_data(condition, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index, update_items = condition.values()
    print(update_index)
    update_index_column = list(update_index.keys())[0]
    update_index_value = list(update_index.values())[0]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(update_items.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                if column == "category":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" category_id = (SELECT id FROM {column} WHERE category = %s )"""
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "client":
                    value = update_items[column]
                    sql_SET = sql_SET + f""" , category_id = (SELECT id FROM {column} WHERE category = %s )"""
                else:
                    value = update_items[column]
                    sql_SET = sql_SET + f"""  , {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        print(sql)
        print(val)
        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount > 0 :
            print(f"update  category {cursor.rowcount} ")
            return 
        else :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
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
    except mysql.connector.Error as e:
        raise e
    finally:
        cursor.close()
        con.close()