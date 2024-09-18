from time import time
import math
from datetime import datetime
from dotenv import load_dotenv
from fastapi import  HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()



def get_data_by_tablename(condition, page, table_name, full_get = None):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        int(page)
        sql = ""
        sql_count = f""" Select count(*) as count from {table_name} 
        """
        if table_name == "client_order":
            sql="""SELECT client_order.id as id, client.name as client, variety.variety_code, amount, creation_date, shipping_date FROM  client_order  
            inner join client 
            on  client_order.client_id =  client.id inner 
            join  variety 
            on client_order.variety_id = variety.id 
            """
        elif table_name == "staff":
            sql = """SELECT staff.employee_id, staff.name, staff.email, staff.cellphone,  staff.in_employment , authorization.job_position  FROM  staff 
            INNER JOIN authorization 
            ON staff.authorization_id = authorization.id"""
        
        elif table_name == "variety":
            sql="""Select variety.variety_code, variety.name, variety.description, category.name as category
            FROM variety 
            INNER JOIN  category
            ON variety.category_id = category.id
            """

        elif table_name == "produce_record":
            sql="""SELECT produce_record.id,  variety.variety_code, variety.name as variety , media.name as media, staff.name as producer, staff.employee_id as employee_id, stage.name as stage, produce_record.produce_date , produce_record.mother_produce_id, produce_record.in_stock,produce_record.consumed_date, produce_record.consumed_reason
            FROM  produce_record 
            INNER JOIN  variety
            ON  produce_record.variety_id = variety.id
            INNER JOIN  media
            ON  produce_record.media_id = media.id
            INNER JOIN  staff
            ON  produce_record.employee_id = staff.id
            INNER JOIN  stage
            ON  produce_record.stage_id = stage.id
            """
        elif table_name == "authorization":
            sql = """SELECT * FROM  authorization"""
        else :
            sql=f"""Select name, description from {table_name}
        """
        data_amount = 0
        sql_limit = str()
        if full_get is None:
            sql_limit = """ limit %s , 10"""
        else:
            sql_limit = ""
        condition_individual = ""
        val = list()
        if condition :
            sql_condition=f"""  where  """
            sql = sql + sql_condition
            
            columns = list(condition.keys())
            columns_set = set(columns)
            client_order_FK_set = {"variety_code", "client"}
            produce_record_FK_set = {"variety_code", "media", "employee_id", "stage",}
            variety_FK_set = {"category"}

            if table_name == "produce_record" and columns_set & produce_record_FK_set:

                sql_join = """
                INNER JOIN  variety
                ON  produce_record.variety_id = variety.id
                INNER JOIN  media
                ON  produce_record.media_id = media.id
                INNER JOIN  staff
                ON  produce_record.employee_id = staff.id
                INNER JOIN  stage
                ON  produce_record.stage_id = stage.id"""
                sql_count = sql_count +  sql_join

            elif table_name == "client_order" and columns_set & client_order_FK_set :

                sql_count = sql_count + """
                inner join client 
                on  client_order.client_id =  client.id inner 
                join  variety 
                on client_order.variety_id = variety.id """
            elif table_name == "variety" and columns_set & variety_FK_set :

                sql_count = sql_count + """
                INNER JOIN  category
                ON variety.category_id = category.id"""
            else:
                sql_count = sql_count + sql_condition        
            for column in columns:
                if columns.index(column) == 0 :
                    if column == "client" or column == "stage" or column == "media" or column =="category":
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
                    elif column == "employee_id":
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
                    elif column == "job_position":
                        sql_sub = f"""select id from authorization where job_position = %s"""
                        val_sub = list()

                        val_sub.append(condition[f"{column}"])
                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        column = "authorization_id"
                        val.append(column_id)
                        condition_individual = f" {table_name}.{column} = %s"
                    elif table_name != "variety" and column == "variety_code":

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
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                            condition[f"{column}"] = 0

                        condition_individual = f" {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                    else:
                        condition_individual = f" {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                    
                else:
                    if column == "client" or column == "stage" or column == "media" or column =="category":
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
                    elif column == "employee_id":
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
                    elif column == "job_position":
                        sql_sub = f"""select id from authorization where job_position = %s"""
                        val_sub = list()
                        val_sub.append(condition[f"{column}"])
                        start = time()
                        cursor.execute(sql_sub, val_sub)
                        end = time()
                        print(f"get id from foreign = %.2f second" % (end -start))
                        column_id = cursor.fetchone()["id"]
                        column = "authorization_id"
                        val.append(column_id)
                        condition_individual = f" AND {table_name}.{column} = %s"
                    elif table_name != "variety" and column == "variety_code":

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
                    elif "in_" in column:
                        if condition[f"{column}"] == "YES":
                            condition[f"{column}"] = 1
                        elif condition[f"{column}"] == "NO":
                            condition[f"{column}"] = 0

                        condition_individual = f" AND {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                    else:
                        condition_individual = f" AND  {table_name}.{column} = %s"
                        val.append(condition[f"{column}"])
                sql = sql + condition_individual
                sql_count = sql_count  + condition_individual  

            count_start = time()

            cursor.execute(sql_count,val)
            count_end = time()
            print(f"get count = %.2f second" % (count_end -count_start))
            count = cursor.fetchall()[0]["count"]
            print("execute count")
            data_amount = count
            sql = sql  + sql_limit
            if full_get is None:
                val.append(page*10)
            data_start = time()
            cursor.execute(sql,val)
            data_end = time()
            print(f"get data = %.2f second" % (data_end -data_start))

            print("execute sql")
        else:
            count_start = time()
            cursor.execute(sql_count)
            count_end = time()
            print(f"get count = %.2f second" % (count_end -count_start))
            print("execute count")
            count = cursor.fetchall()[0]["count"]
            data_amount = count
            sql = sql  + sql_limit
            if full_get is None:
                val.append(page*10)
            data_start = time()
            cursor.execute(sql,val) 
            data_end = time()
            print(f"get data = %.2f second" % (data_end -data_start))
            print("execute sql")
        result = cursor.fetchall()
        for data in result:
            keys = data.keys()
            for key in keys:
                if "date" in key:
                    if data[f"{key}"] is None:
                        continue
                    else:
                        data[f"{key}"] = datetime.strftime(data[f"{key}"], "%Y-%m-%d")
        response = {}
        page_amount = math.ceil(data_amount/10)
        response["PageAmount"] = page_amount
        response["dataAmount"] = data_amount
        response["startPage"] = page
        response["data"] = result
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

