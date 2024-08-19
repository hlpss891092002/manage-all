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
        sql_count = f""" Select count(id) as count from {table_name} 
        """
        if table_name == "client_order":
            sql="""SELECT client_order.id as order_id, client.name as client, variety.variety_code, amount, creation_date, shipping_date FROM  client_order  
            inner join client 
            on  client_order.client_id =  client.id inner 
            join  variety 
            on client_order.variety_id = variety.id 
            """

            # sql_count = f""" Select client_order.id from client_order  
            # inner join client 
            # on  client_order.client_id =  client.id inner 
            # join  variety 
            # on client_order.variety_id = variety.id """
        elif table_name == "staff":
            sql = """SELECT staff.employee_id, staff.name, staff.email, staff.cellphone,  staff.in_employment , authorization.job_position  FROM  staff 
            INNER JOIN authorization 
            ON staff.authorization_id = authorization.id"""

            # sql_count = f""" Select id from {table_name}"""
        
        elif table_name == "variety":
            sql="""Select variety.variety_code, variety.name, variety.description, category.name as category
            FROM variety 
            INNER JOIN  category
            ON variety.category_id = category.id
            """

            # sql_count = f""" Select variety.id from {table_name} INNER JOIN  category
            # ON variety.category_id = category.id"""
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


        else :
            sql=f"""Select name, description from {table_name}
        """
            # sql_count = f""" Select id from {table_name}"""
        data_amount = 0
        # sql_count_limit = " limit 101"
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
                    print(column, condition[column])
                    if column == "client" or column == "stage" or column == "media" or column =="category":
                        print(column)
                        sql_sub = f"""select id from {column} where name = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        column = column + "_id"
                        condition_individual = f" {table_name}.{column} = %s"
                        column = column.replace("_id", "")                   
                        print(column)
                    elif column == "producer_id":
                        sql_sub = f"""select id from staff where employee_id = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        condition_individual = f" {table_name}.{column} = %s"
                    elif table_name != "variety" and column == "variety_code":
                        print(column)
                        sql_sub = f"""select id from variety where {column} = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        column = "variety_id"
                        condition_individual = f" {table_name}.{column} = %s"
                    elif "in_" in column:
                        print(column)
                        print(condition[f"{column}"])
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                            condition[f"{column}"] = 0
                        print(condition[f"{column}"])
                        condition_individual = f" {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                    else:
                        condition_individual = f" {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                    
                else:
                    if column == "client" or column == "stage" or column == "media" or column =="category":
                        print(column)
                        sql_sub = f"""select id from {column} where name = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        column = column + "_id"
                        condition_individual = f" AND {table_name}.{column} = %s"
                        column = column.replace("_id", "")                   
                        print(column)
                    elif column == "producer_id":
                        sql_sub = f"""select id from staff where employee_id = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        condition_individual = f"  AND  {table_name}.{column} = %s"
                    elif table_name != "variety" and column == "variety_code":
                        print(column)
                        sql_sub = f"""select id from variety where {column} = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])

                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        val.append(column_id)
                        column = "variety_id"
                        condition_individual = f" AND  {table_name}.{column} = %s"
                    else:
                        condition_individual = f" AND  {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                sql = sql + condition_individual
                sql_count = sql_count  + condition_individual  
            # print(sql)
            
            # print(val)
            count_start = time()
            cursor.execute(sql_count,val)
            count_end = time()
            print(f"get count = %.2f second" % (count_end -count_start))
            count = cursor.fetchall()[0]["count"]
            print("execute count")
            data_amount = count
            sql = sql  + sql_limit
            val.append(page*30)
            data_start = time()
            cursor.execute(sql,val)
            data_end = time()
            print(f"get data = %.2f second" % (data_end -data_start))
            # print(sql)
            print("execute sql")
        else:
            # print(sql)
            print(sql_count) 
            count_start = time()
            cursor.execute(sql_count)
            count_end = time()
            print(f"get count = %.2f second" % (count_end -count_start))
            print("execute count")
            count = cursor.fetchall()[0]["count"]
            data_amount = count
            sql = sql  + sql_limit
            val.append(page*30)
            data_start = time()
            cursor.execute(sql,val) 
            data_end = time()
            print(f"get data = %.2f second" % (data_end -data_start))
            print("execute sql")
        print(f"sql_count  : {sql_count}")
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
        # if data_amount < 100:
        response["dataAmount"] = data_amount
        # else:
        #     response["dataAmount"] = "100+"
        
        response["startPage"] = page
        response["data"] = result
        print(f"sql  : {sql}")
        print(f"sql_count  : {sql_count}")
        print(f"val {val}")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()
