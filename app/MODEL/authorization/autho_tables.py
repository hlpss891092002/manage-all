
from fastapi import HTTPException
from app.model.db import DB

#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def show_table():
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary=True, buffered = True)
    try:
        sql = """SHOW TABLES 
         """
        cursor.execute(sql)
        result = cursor.fetchall()
        table_list = []
        for table in result:
            tableName = table["Tables_in_manageall_database"]
            if tableName == "authorization":
                continue
            table_list.append(tableName)
        table_list.sort()

        return table_list
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        con.close()

def get_table_list_from_auth( employee_id):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary=True, buffered = True)
 
    try:
        sql = """SELECT  authorization, category, client, client_order, media, produce_record, staff, stage, variety FROM staff
        INNER JOIN authorization
        ON staff.authorization_id = authorization.id
        WHERE employee_id = %s
         """
        val = (employee_id,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        cursor.close()
        con.close()

