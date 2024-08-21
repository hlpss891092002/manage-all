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


def update_non_foreign_key_data(condition, table_name, index_value):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    print(condition)
    print(table_name)
    print(index_value)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    print(update_index_value)
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                value = condition[column]
                sql_SET = sql_SET + f"""  {column} = %s """
                val.append(value)
            else:
                 value = condition[column]
                 sql_SET = sql_SET + f""" , {column}  = %s """ 
                 val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        print(sql)
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

def update_client_order_data(condition, table_name, index_value):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    print(update_index_value)
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where id = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                if column == "client":
                    value = condition[column]
                    sql_SET = sql_SET + f""" client_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = condition[column]
                    sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                else:
                    value = condition[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "client":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , client_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                else:
                    value = condition[column]
                    sql_SET = sql_SET + f"""  , {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
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

def update_produce_record_data(condition, table_name, index_value):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    print(update_index_value)
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            print(column)
            if column_list.index(column) == 0:
                if column == "media":
                    value = condition[column]
                    sql_SET = sql_SET + f""" media_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = condition[column]
                    sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                elif column == "producer_id":
                    value = condition[column]
                    sql_SET = sql_SET + f""" producer_id = (SELECT id FROM staff WHERE employee_id = %s )"""
                elif column == "stage":
                    value = condition[column]
                    sql_SET = sql_SET + f""" stage_id = (SELECT id FROM stage WHERE name = %s )"""
                elif column == "in_stock":
                    print(column)
                    value =condition[column]
                    if value == "YES":
                        value = 1
                    elif value == "NO":
                        value = 0
                    else:
                        return
                    sql_SET = sql_SET + f"""  {column} = %s """
                else:
                    value = condition[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "media":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , media_id = (SELECT id FROM {column} WHERE name = %s )"""
                elif column == "variety_code":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
                elif column == "producer_id":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , producer_id = (SELECT id FROM staff WHERE employee_id = %s )"""
                elif column == "stage":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , stage_id = (SELECT id FROM stage WHERE name = %s )"""
                elif column == "in_stock":
                    print(column)
                    value =condition[column]
                    if value == "YES":
                        value = 1
                    elif value == "NO":
                        value = 0
                    else:
                        return
                    sql_SET = sql_SET + f""" ,  {column} = %s """
                else:
                    value = condition[column]
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

def update_variety_data(condition, table_name, index_value):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    print(update_index_value)
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            if column_list.index(column) == 0:
                if column == "category":
                    value = condition[column]
                    sql_SET = sql_SET + f""" category_id = (SELECT id FROM {column} WHERE category = %s )"""
                else:
                    value = condition[column]
                    sql_SET = sql_SET + f"""  {column} = %s """
            else:
                if column == "client":
                    value = condition[column]
                    sql_SET = sql_SET + f""" , category_id = (SELECT id FROM {column} WHERE category = %s )"""
                else:
                    value = condition[column]
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
