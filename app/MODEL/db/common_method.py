import mysql.connector

from time import time
from datetime import date, timedelta
from fastapi import  HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def get_table_columns(table_name):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql=f"""SHOW COLUMNS FROM {table_name};
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        columns_list = []
        for column in result:
            columnName = column["Field"]
            if columnName == "mother_produce_id" or columnName == "employee_id" :
                columns_list.append(columnName)
                continue
            elif columnName == "variety_id":
                columnName = columnName.replace("_id", "_code")
                columns_list.append(columnName)
                continue
            columnName = column["Field"].replace("_id", "")
            columns_list.append(columnName)
        return(columns_list)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        con.close()

def get_foreign_column(table_name):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql = """
                SELECT     COLUMN_NAME 
                FROM  INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                
                WHERE
                TABLE_NAME = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL
                AND TABLE_SCHEMA = "manageall_database"
                """
        val = list()
        
        val.append(table_name)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        column_list = list()
        for column in result:
            column_list.append(column["COLUMN_NAME"])
        return column_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def get_column_value_distinct(column):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        if column == "mother_produce_id":
            return
        elif column =="employee_id":
            FK_table = "staff"
        else:
            FK_table = column.replace("_id", "")

        if FK_table == "variety":
            FK_column = "variety_code"
        elif FK_table == "staff":
            FK_column = column
        elif FK_table == "authorization":
            FK_column = "job_position"
        else:
            FK_column = "name"
        
        sql = f"""
                SELECT  DISTINCT {FK_table}.{FK_column} FROM {FK_table}
                
                """ 
        cursor.execute(sql)
        result = cursor.fetchall()
        value_list= list()
        for key_pair in result:
            value = list(key_pair.values())[0]
            value_list.append(value)  
        return value_list

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

#for mainpage
def get_yesterday_produce_category():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        yesterday = now - timedelta(days=1)

        sql="""SELECT category.name as category,  count(produce_record.id) as count
        FROM produce_record        
        inner JOIN variety
        ON produce_record.variety_id = variety.id 
        INNER JOIN category
        ON variety.category_id = category.id  
        where produce_date = %s  and in_stock = 1
        group by category.name
        
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
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()
        yesterday = now - timedelta(days=1)
        sql="""SELECT category.name as category,  count(produce_record.id) as count 
        FROM produce_record
        inner JOIN variety
        ON produce_record.variety_id = variety.id  
        INNER JOIN category
        ON variety.category_id = category.id
        where in_stock = 1 
        group by category.name 
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
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()

        # shipping_date_diff = now - timedelta(weeks=4)
        sql="""SELECT category.name as category,   count(produce_record.id) as count 
        FROM produce_record
        inner JOIN variety
        ON produce_record.variety_id = variety.id
        INNER JOIN category
        ON variety.category_id = category.id 
        where in_stock = 1   and stage_id = 5  and DATEDIFF(%s, produce_date) > 30
        group by category;
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

def get_seven_days_outs():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()

        # shipping_date_diff = now - timedelta(weeks=4)
        sql="""SELECT  produce_date,  count(produce_record.id) as count 
        FROM produce_record
        inner JOIN variety
        ON produce_record.variety_id = variety.id
        where in_stock = 1    and DATEDIFF(%s, produce_date) <= 7
        group by  produce_date;
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

def optimize_index():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        now = date.today()

        sql="""OPTIMIZE TABLE produce_record;
        """
        cursor.execute(sql)
        print("OPTIMIZE complete")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def recreate_produce_record():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql=f"""CREATE TABLE backup AS SELECT * FROM produce_record;
        drop table produce_record;
        RENAME TABLE backup to produce_record;
        """
        sql_alter_PK="""ALTER TABLE produce_record
                        ADD PRIMARY KEY (id);"""
        sql_alter_variety="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_variety_produce_record
            FOREIGN KEY (variety_id)
            REFERENCES variety(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;
            """
        sql_alter_media="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_media_produce_record
            FOREIGN KEY (media_id)
            REFERENCES media(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;"""
        sql_alter_staff="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_staff_produce_record
            FOREIGN KEY (employee_id)
            REFERENCES staff(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;"""
        sql_alter_stage="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_stage_produce_record
            FOREIGN KEY (stage_id)
            REFERENCES stage(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;"""
        sql_alter_mother_id="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_mother_produce_id
            FOREIGN KEY (mother_produce_id)
            REFERENCES produce_record(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE"""
        cursor.execute(sql)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()
