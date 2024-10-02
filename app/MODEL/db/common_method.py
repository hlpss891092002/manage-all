import mysql.connector

from time import time
from datetime import date, timedelta
from fastapi import  HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def timeit(func):
    start_time = time()
    result = func()
    end_time = time()
    execute_time = end_time - start_time
    print(f"{func.__name__} executed in {execute_time:.4f} seconds")
    return result

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
        sql_create_backup=f"""
        CREATE TABLE backup AS SELECT * FROM produce_record;
        """
        sql_drop_produce = "DROP TABLE produce_record;"
        sql_rename_backup = "RENAME TABLE backup TO produce_record;"

        cursor.execute(sql_create_backup)
        print("Created backup table.")
        
        cursor.execute(sql_drop_produce)
        print("Dropped produce_record table.")
        
        cursor.execute(sql_rename_backup)
        print("Renamed backup table to produce_record.")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def set_key_on_produce_record_created():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql_alter_PK="""
            ALTER TABLE produce_record
            ADD PRIMARY KEY (id);"""
        sql_alter_variety="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_variety_produce_record
            FOREIGN KEY (variety_id)
            REFERENCES variety(id)
            ON UPDATE CASCADE;
            """
        sql_alter_media="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_media_produce_record
            FOREIGN KEY (media_id)
            REFERENCES media(id)
            ON UPDATE CASCADE;"""
        sql_alter_staff="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_staff_produce_record
            FOREIGN KEY (employee_id)
            REFERENCES staff(id)
            ON UPDATE CASCADE;"""
        sql_alter_stage="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_stage_produce_record
            FOREIGN KEY (stage_id)
            REFERENCES stage(id)
            ON UPDATE CASCADE;"""
        sql_alter_mother_id="""
            ALTER TABLE produce_record
            ADD CONSTRAINT fk_mother_produce_id
            FOREIGN KEY (mother_produce_id)
            REFERENCES produce_record(id)
            ON DELETE SET NULL;
            """
        cursor.execute(sql_alter_PK)
        print("Set primary key")
        cursor.execute(sql_alter_variety)
        print("Set foreign key on variety")
        cursor.execute(sql_alter_media)
        print("Set foreign key on media")
        cursor.execute(sql_alter_staff)
        print("Set foreign key on staff")
        cursor.execute(sql_alter_stage)
        print("Set foreign key on stage")
        cursor.execute(sql_alter_mother_id)
        print("Set foreign key on mother_id")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def set_indexed_on_produce_record_created():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try:
        sql_begin = "begin;"
        sql_index_produce_record_variety_id_composite = """
            CREATE INDEX idx_produce_record_variety_id_composite
            ON produce_record(variety_id, media_id, employee_id, stage_id, produce_date, in_stock,consumed_date, consumed_reason);
        """
        sql_index_produce_record_media_id_composite = """
            CREATE INDEX idx_produce_record_media_id_composite
            ON produce_record( media_id, employee_id, stage_id, produce_date, in_stock,consumed_date, consumed_reason);
        """
        sql_index_produce_record_employee_id_composite = """
            CREATE INDEX idx_produce_record_employee_id_composite
            ON produce_record(employee_id, stage_id, produce_date, in_stock,consumed_date, consumed_reason);
        """
        sql_index_produce_record_stage_id_composite = """
            CREATE INDEX idx_produce_record_stage_id_composite
            ON produce_record(stage_id, produce_date, in_stock,consumed_date, consumed_reason);
        """
        sql_index_produce_record_produce_date_composite = """
            CREATE INDEX idx_produce_record_produce_date_composite
            ON produce_record(produce_date, in_stock, consumed_date, consumed_reason);
        """
        sql_index_produce_record_in_stock_composite = """
            CREATE INDEX idx_produce_record_in_stock_composite
            ON produce_record(in_stock, consumed_date, consumed_reason);
        """
        sql_index_produce_record_consumed_date_composite = """
            CREATE INDEX idx_produce_record_consumed_date_composite
            ON produce_record(consumed_date, consumed_reason);
        """
        sql_index_produce_record_consumed_reason = """
            CREATE INDEX idx_produce_record_produce_consumed_reason
            ON produce_record(consumed_reason);
        """
        sql_commit = """
                        commit;
                        """
        cursor.execute(sql_begin)
        cursor.execute(sql_index_produce_record_variety_id_composite)
        cursor.execute(sql_index_produce_record_media_id_composite)
        cursor.execute(sql_index_produce_record_employee_id_composite)
        cursor.execute(sql_index_produce_record_stage_id_composite)
        cursor.execute(sql_index_produce_record_produce_date_composite)
        cursor.execute(sql_index_produce_record_in_stock_composite)
        cursor.execute(sql_index_produce_record_consumed_date_composite)
        cursor.execute(sql_index_produce_record_consumed_reason)
        cursor.execute(sql_commit)
        
        print("Set all index on produce record")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

