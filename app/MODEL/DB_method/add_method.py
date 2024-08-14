import mysql.connector
import mysql.connector.pooling
import os
from fastapi import HTTPException
from time import time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

#create connection pool
try:
    dbconfig = {
        "host": os.getenv("DBHOST"),
        "user": os.getenv("DBUSER"),
        "password": os.getenv("DBPASSWORD"),
        "database":"manageall_database",
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        **dbconfig
    )

    # print("database connected")
    
except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

def insert_authorization(job_position, authorization, category, client, client_order, media, produce_record, staff, stage, variety):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO authorization(job_position, authorization, category, client, client_order, media, produce_record, staff, stage, variety)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        val=(job_position, authorization, category, client, client_order,  media, produce_record, staff, stage, variety)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {job_position} authorization")
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def insert_tableName_data(input_dict, tableName):
    # category, description = input_dict.values()
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql = f"""INSERT INTO {tableName} ( """
        sql_val = """ VALUES ( """
        columns = list(input_dict.keys())
        val = list()
        for column in columns:
            print(column)
            if columns.index(column) == len(columns) - 1:
                sql = sql + " , " + str(column) + " )"
                sql_val = sql_val + ", %s )"  
            elif columns.index(column) == 0 :
                 sql = sql + str(column)
                 sql_val = sql_val + " %s " 
            else:
                sql = sql  + " , " + str(column)
                sql_val = sql_val + ", %s "
            val.append(input_dict[column])
        sql = sql + sql_val
        cursor.execute(sql,val)
        con.commit()
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def insert_client_order(input_dict, tableName):
    client, variety, amount,  shipping_date = input_dict.values()
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql=f"""INSERT INTO {tableName} (client_id, variety_id, amount, shipping_date)
        VALUES ((SELECT id from client WHERE name =  %s), (SELECT id from variety WHERE variety_code =  %s), %s, %s);
        """
        val=(client, variety, amount, shipping_date)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {client}, {amount} in order")
        return True
    except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def insert_produce_record(input_dict , in_stock = True):
    print(input_dict)
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    id, variety, media, producer_id, stage, mother_produce_id, consumed_reason = input_dict.values()
    try:
        sql="""INSERT INTO produce_record(id, variety_id, media_id, stage_id, mother_produce_id, in_stock, consumed_reason, producer_id)
        VALUES (%s, (SELECT id FROM variety where variety_code = %s), (SELECT id FROM media where name = %s), (SELECT id FROM stage where name = %s), %s, %s, %s, (SELECT id FROM staff where employee_id = %s));
        """
        val=(id, variety, media, stage, mother_produce_id, in_stock, consumed_reason, producer_id)
        cursor.execute(sql,val)
        con.commit()
        # print(f"insert {id} production")
        return True
    except Exception as e:
            print(f"{e}")
            raise HTTPException(status_code=400, detail=f"{e}")
        # return False
    finally:
        cursor.close()
        con.close()

def insert_staff( input_dict, in_employment = True):
    name, email, cellphone, employee_id, password, job_position =input_dict.values()
    print(name, email, cellphone, employee_id, password, job_position)
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO staff(name, email, cellphone, employee_id, password, authorization_id, in_employment )
        VALUES ( %s, %s, %s, %s, %s, (SELECT id FROM authorization WHERE  job_position = %s), %s);
        """
        val=(name, email, cellphone, employee_id, password, job_position,in_employment)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {id} staff")
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def insert_variety(input_dict):
    variety_code, name, description, category = input_dict.values()
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO variety(variety_code, name, description, category_id)
        VALUES (%s, %s, %s, (SELECT id FROM category  WHERE category =  %s));
        """
        val=(variety_code, name, description, category)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {variety_code} variety")
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def consume_mother_stock(mother_produce_id, consumed_reason, in_stock = False ):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql1="""UPDATE produce_record   
        SET in_stock = %s, consumed_reason = %s 
        WHERE id = %s
        """
        val1=( in_stock, consumed_reason, mother_produce_id)
       
        cursor.execute(sql1,val1)
        con.commit()
        print(f"delete {mother_produce_id} stock")
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()
