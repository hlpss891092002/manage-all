from app.model.db import DB


#DB instantiated
myDB = DB.DB(database = "manageall_database")
myDB.initialize()

def check_user(employee_id, password):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try: 
      sql = """ SELECT employee_id, staff.name as name, authorization.job_position as job_position FROM staff
      inner join authorization
      on staff.authorization_id = authorization.id    
      where employee_id = %s and password = %s"""
      val = (employee_id, password)
      cursor.execute(sql,val)
      result = cursor.fetchone()
      return (result)
    except Exception as e:
        pass
    finally:
      cursor.close()
      con.close()


def get_user_data(employee_id, password):
    con = myDB.cnx_pool.get_connection()
    cursor = con.cursor(dictionary = True, buffered = True)
    try: 
      sql = """ SELECT staff.employee_id, staff.name, staff.email, staff.cellphone, authorization.authorization, authorization.job_position FROM staff
        INNER JOIN authorization
        ON staff.authorization_id = authorization.id
        WHERE staff.id = %s AND staff.password = %s
      """
      val = (employee_id, password)
      cursor.execute(sql,val)
      result = cursor.fetchone()
      return (result)
    except Exception as e:
        pass
    finally:
      con.close()
      cursor.close()