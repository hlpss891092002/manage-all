import mysql.connector
import mysql.connector.pooling
import os
from time import time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

#create connection pool
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

def insert_authorization(job_position, authorization):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO authorization(job_position, authorization)
        VALUES (%s, %s);
        """
        val=(job_position, authorization)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {job_position} authorization")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_staff( name, email, cellphone, account, password, authorization_id, in_employment = True):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO staff(name, email, cellphone, account, password, authorization_id, in_employment )
        VALUES ( %s, %s, %s, %s, %s, %s, %s);
        """
        val=(name, email, cellphone, account, password, authorization_id,in_employment)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {id} staff")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_media(media_name, description):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO media(media_name, description)
        VALUES (%s, %s);
        """
        val=(media_name, description)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {media_name} media")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_stage(stage_name, description):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO stage(stage_name, description)
        VALUES (%s, %s);
        """
        val=(stage_name, description)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {stage_name} stage")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_category(category, description):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO category(category, description)
        VALUES (%s, %s);
        """
        val=(category, description)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {category} category")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_client(name, description):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO client(name, description)
        VALUES (%s, %s);
        """
        val=(name, description)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {id} client")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_variety(variety_code, name, description, photo, category_id):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO variety(variety_code, name, description, photo, category_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        val=(variety_code, name, description, photo, category_id)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {variety_code} variety")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_order(client_id, variety_id, amount,  shipping_date):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO client_order(client_id, variety_id, amount, shipping_date)
        VALUES (%s, %s, %s,%s);
        """
        val=(client_id, variety_id, amount,  shipping_date)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {client_id}, {amount} in order")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_production(id, variety_id, media_id, producer_id, stage_id, mother_produce_id = None, consumed_reason = None , in_stock = True):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO produce_record(id, variety_id, media_id, stage_id, mother_produce_id, in_stock, consumed_reason, producer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT id FROM staff where account = %s));
        """
        val=(id, variety_id, media_id, stage_id, mother_produce_id, in_stock, consumed_reason, producer_id)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {id} production")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def insert_current_stock(record_id):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql="""INSERT INTO current_stock(produce_record_id)
        VALUES (%s);
        """
        val=(record_id,)
        cursor.execute(sql,val)
        con.commit()
        print(f"insert {record_id} stock")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()

def consume_mother_stock(record_id, consumed_reason, in_stock = False ):
    con = connection_pool.get_connection()
    cursor = con.cursor(dictionary = True)
    try:
        sql1="""UPDATE produce_record   
        SET in_stock = %s, consumed_reason = %s 
        WHERE id = %s
        """
        val1=( in_stock, consumed_reason, record_id)
        sql2="""DELETE FROM current_stock WHERE produce_record_id = %s
        """
        val2=(record_id,)
        cursor.execute(sql1,val1)
        cursor.execute(sql2,val2)
        con.commit()
        # print(f"insert {record_id} stock")
        return True
    except Exception as e:
        print(f"{e}")
        return False
    finally:
        cursor.close()
        con.close()
