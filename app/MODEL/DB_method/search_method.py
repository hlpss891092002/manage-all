import mysql.connector
import mysql.connector.pooling
import os
from time import time
import math
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


def get_data_by_tablename(condition, page, table_name):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        int(page)
        sql = ""
        # sql_order = ""
        if table_name == "client_order":
            sql="""SELECT client_order.id as order_id, client.name as client, variety.variety_code, amount, creation_date, shipping_date FROM  client_order  
            inner join client 
            on  client_order.client_id =  client.id inner 
            join  variety 
            on client_order.variety_id = variety.id 
        """
            sql_order = " ORDER BY client_order.id DESC"
            sql_count = f""" Select client_order.id from client_order  
            inner join client 
            on  client_order.client_id =  client.id inner 
            join  variety 
            on client_order.variety_id = variety.id """
        elif table_name == "staff":
            sql = """SELECT staff.employee_id, staff.name, staff.email, staff.cellphone,  staff.in_employment , authorization.job_position  FROM  staff 
            INNER JOIN authorization 
            ON staff.authorization_id = authorization.id"""
            sql_order = " ORDER BY staff.id DESC"
            sql_count = f""" Select id from {table_name}"""
        elif table_name == "category":
            sql=f"""Select category, description from {table_name}
        """
            sql_order = "  ORDER BY id DESC"
            sql_count = f""" Select id from {table_name}"""
        elif table_name == "variety":
            sql="""Select variety.variety_code, variety.name, variety.description, category.category
            FROM variety 
            INNER JOIN  category
            ON variety.category_id = category.id
            """
            sql_order = " ORDER BY variety.id DESC"
            sql_count = f""" Select variety.id from {table_name} INNER JOIN  category
            ON variety.category_id = category.id"""
        elif table_name == "produce_record":
            sql="""SELECT produce_record.id,  variety.variety_code, variety.name as variety , media.name as media, staff.name as producer, staff.employee_id as producer_id, stage.name as stage, produce_record.manufacturing_date , produce_record.mother_produce_id, produce_record.in_stock, produce_record.consumed_reason
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
            sql_order = " ORDER BY produce_record.manufacturing_date DESC"
            sql_count = f""" Select produce_record.variety_id from produce_record INNER JOIN  variety
            ON  produce_record.variety_id = variety.id
            INNER JOIN  media
            ON  produce_record.media_id = media.id
            INNER JOIN  staff
            ON  produce_record.producer_id = staff.id
            INNER JOIN  stage
            ON  produce_record.stage_id = stage.id
            """
        else :
            sql=f"""Select name, description from {table_name}
        """
            sql_order = "  ORDER BY id DESC"
            sql_count = f""" Select id from {table_name}"""
        data_amount = 0
        sql_count_limit = " limit 101"
        sql_limit = """ limit %s , 10"""
        condition_individual = ""
        val = list()
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            sql_count = sql_count + sql_condition
            columns = list(condition.keys())
            
            for column in columns:
                print(column, columns.index(column))
                if columns.index(column) == 0 :
                    print("1")
                    if table_name == "client_order":
                        if column == "variety_code":
                            condition_individual=f""" variety.{column} = %s"""
                        elif column == "client":
                            condition_individual=f""" {column}.name = %s"""
                        else:
                            condition_individual=f""" client_order.{column} = %s"""
                    elif table_name == "variety":
                        if column == "category":
                            condition_individual=f""" category.{column} = %s"""
                        else:
                            condition_individual=f""" variety.{column} = %s"""
                    elif table_name == "produce_record":
                        if column == "id" or column == "manufacturing_date" or column == "mother_produce_id" or column == "consumed_reason" :
                            condition_individual=f""" produce_record.{column} = %s"""
                        elif column == "producer_id":
                            condition_individual=f""" staff.employee_id = %s"""
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
                    else:
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
                    print("2")
                    if table_name == "client_order":
                        if column == "variety_code":
                            condition_individual=f""" AND variety.{column} = %s"""
                        elif column == "client":
                            condition_individual=f""" AND {column}.name = %s"""
                        else:
                            condition_individual=f""" AND client_order.{column} = %s""" 
                    elif table_name == "variety":
                        if column == "category":
                            condition_individual=f""" AND category.{column} = %s"""
                        else:
                            condition_individual=f""" AND variety.{column} = %s"""
                    elif table_name == "produce_record":
                        print("3")
                        if column == "id" or column == "manufacturing_date" or column == "mother_produce_id" or column == "consumed_reason" :
                            condition_individual=f""" AND produce_record.{column} = %s"""
                        elif column == "producer_id":
                            condition_individual=f""" AND staff.employee_id = %s"""
                        elif column == "variety_code":
                            
                            condition_individual=f""" AND variety.variety_code = %s"""
                        elif column == "in_stock":
                            print("4")
                            if condition[f"{column}"] == "YES":
                                condition[f"{column}"] = 1
                            elif condition[f"{column}"] == "NO":
                                condition[f"{column}"] = 0
                            condition_individual=f""" AND produce_record.{column} = %s"""
                        else:
                            condition_individual=f""" AND {column}.name = %s"""
                    else:
                        print("in_employment yes")
                        if column == "in_employment":
                            if condition[f"{column}"] == "YES":
                                condition[f"{column}"] = 1
                            elif condition[f"{column}"] == "NO":
                                condition[f"{column}"] = 0
                            condition_individual=f""" AND {column} = %s"""
                        else:
                            condition_individual=f""" AND {column} = %s"""
                val.append(condition[f"{column}"])
                sql = sql + condition_individual
                sql_count = sql_count  + condition_individual  
            sql_count = sql_count +  sql_count_limit
            print(sql_count)
            cursor.execute(sql_count,val)
            print(sql_count)
            print("execute sql_count")
            count = len(cursor.fetchall())
            data_amount = count
            sql = sql  + sql_limit
            val.append(page*30)
            cursor.execute(sql,val)
            print(sql)
            print("execute sql")
        else: 
            sql_count = sql_count +  sql_count_limit
            cursor.execute(sql_count)
            print("execute sql_count")
            count = len(cursor.fetchall())
            print(count)
            data_amount = count
            sql = sql + sql_limit
            val.append(page*30)
            cursor.execute(sql,val) 
            print("execute sql")
        result = cursor.fetchall()
        print(len(result))
        for data in result:
            keys = data.keys()
            for key in keys:
                if "date" in key:
                    data[f"{key}"] = datetime.strftime(data[f"{key}"], "%Y-%m-%d")
        response = {}
        page_amount = math.ceil(data_amount/10)
        response["PageAmount"] = page_amount
        if data_amount < 100:
            response["dataAmount"] = data_amount
        else:
            response["dataAmount"] = "100+"
        
        response["startPage"] = page
        response["data"] = result

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()
