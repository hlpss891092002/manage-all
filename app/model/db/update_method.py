import mysql.connector
from fastapi import  HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def update_non_foreign_key_data(condition, table_name, index_value):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            column_num = column_list.index(column)
            if column_num > 0:
                sql_SET = sql_SET + " , " 
            value = condition[column]
            sql_SET = sql_SET + f"""  {column} = %s """
            val.append(value)

        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        cursor.execute(sql,val)
        con.commit()
        if cursor.rowcount == 0 :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update, please check input value")
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

def update_client_order_data(condition, table_name, index_value):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where id = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            column_num = column_list.index(column)
            if column_num > 0:
                sql_SET = sql_SET + " , " 
            if column == "client":
                value = condition[column]
                sql_SET = sql_SET + f""" client_id = (SELECT id FROM {column} WHERE name = %s )"""
            elif column == "variety_code":
                value = condition[column]
                sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
            else:
                value = condition[column]
                sql_SET = sql_SET + f"""  {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount == 0 :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
    finally:
        cursor.close()
        con.close()

def update_produce_record_data(condition, table_name, index_value):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            column_num = column_list.index(column)
            if column_num > 0:
                sql_SET = sql_SET + " , " 
            if column == "media":
                value = condition[column]
                sql_SET = sql_SET + f""" media_id = (SELECT id FROM {column} WHERE name = %s )"""
            elif column == "variety_code":
                value = condition[column]
                sql_SET = sql_SET + f""" variety_id = (SELECT id FROM variety WHERE {column} = %s )"""
            elif column == "employee_id":
                value = condition[column]
                sql_SET = sql_SET + f""" employee_id = (SELECT id FROM staff WHERE employee_id = %s )"""
            elif column == "stage":
                value = condition[column]
                sql_SET = sql_SET + f""" stage_id = (SELECT id FROM stage WHERE name = %s )"""
            elif column == "in_stock":
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
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)
        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount == 0 :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
    finally:
        cursor.close()
        con.close()

def update_variety_data(condition, table_name, index_value):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            column_num = column_list.index(column)
            if column_num > 0:
                sql_SET = sql_SET + " , " 
            if column == "category":
                value = condition[column]
                sql_SET = sql_SET + f""" category_id = (SELECT id FROM {column} WHERE category = %s )"""
            else:
                value = condition[column]
                sql_SET = sql_SET + f"""  {column} = %s """
            val.append(value)
        sql = sql + sql_SET + sql_condition
        val.append(update_index_value)

        cursor.execute(sql,val)
        con.commit() 
        if cursor.rowcount == 0 :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the update. Please check input value")

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Value in client or variety is invalid. Please check input value")
    finally:
        cursor.close()
        con.close()

def update_staff_data(condition, table_name, index_value):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    update_index_value = index_value
    update_index_column = condition["indexColumn"]
    del condition["indexColumn"]
    try:
        sql=f"""UPDATE {table_name}"""
        sql_condition=f" where {update_index_column} = %s"
        sql_SET =" SET"
        val = list()
        column_list = list(condition.keys())
        for column in column_list:
            column_num = column_list.index(column)
            if column_num > 0:
                sql_SET = sql_SET + " , " 
            if column == "job_position":
                value = condition[column]
                sql_SET = sql_SET + f""" authorization_id = (SELECT id FROM authorization WHERE {column} = %s )"""
            else:
                value = condition[column]
                sql_SET = sql_SET + f"""  {column} = %s """
               
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
