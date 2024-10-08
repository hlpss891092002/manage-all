import mysql.connector
from time import time
from fastapi import  HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def delete_data(condition, table_name):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    delete_index_column= list(condition.keys())[0]
    values = condition[delete_index_column]
    try:
        val = list(values)
        sql = f"""DELETE FROM  {table_name} """
        sql_condition = ""
        if len(val) > 1 :
            sql_condition = f"""WHERE {table_name}.{delete_index_column} in ("""
            valNum = len(val)
            count = 0
            while  count < valNum:
                if count == 0 :
                    sql_condition = sql_condition + " %s"
                elif count == len(val)-1:
                    sql_condition = sql_condition + ", %s)"
                else:
                    sql_condition = sql_condition + ", %s "
                count +=1
        else:
            sql_condition = f"""WHERE {table_name}.{delete_index_column}  = %s"""
        sql = sql + sql_condition
        cursor.execute(sql,val)
        con.commit()
        if cursor.rowcount == 0 :
            raise HTTPException(status_code=400, detail=f"No rows were affected by the delete, please check input value")
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

