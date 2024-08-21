import logging
import mysql.connector
import mysql.connector.pooling
from dotenv import load_dotenv
import os

load_dotenv()

def connection():
    try:
        dbconfig = {
            'host': os.getenv('DBHOST'),
            'user': os.getenv('DBUSER'),
            'password': os.getenv('DBPASSWORD'),
            'database':'manageall_database',
        }
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name='mypool',
            pool_size=3,
            **dbconfig
        )
        cnx1 = cnxpool.get_connection()
        print('database connected')
        return cnx1
    except Exception as e:
        print(f'database connection fail {e}')

def create_table(sql):
    con = connection()
    cursor = con.cursor(dictionary = True)
    try:
        cursor.execute(sql)
        print(f"execute {sql} over")
    except Exception as e:
        print(f"{e}")
    finally:
        cursor.close()
        con.close()

simple_sql_authorization_level = """CREATE TABLE authorization(
            id BIGINT auto_increment, 
            job_position varchar(100) NOT NULL,
            authorization bool NOT NULL,
            category bool NOT NULL, 
            client bool NOT NULL, 
            client_order bool NOT NULL, 
            media bool NOT NULL, 
            produce_record bool NOT NULL, 
            staff bool NOT NULL, 
            stage bool NOT NULL, 
            variety bool NOT NULL,
            PRIMARY KEY(id)
)"""


sql_staff ="""CREATE TABLE staff(
            id BIGINT auto_increment,
            name varchar(255) NOT NULL,
            email varchar(255),
            cellphone varchar(10),       
            employee_id varchar(255) NOT NULL UNIQUE,
            password varchar(255) NOT NULL,
            authorization_id BIGINT NOT NULL,
            in_employment bool NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY (authorization_id) REFERENCES authorization(id)        
)"""


simple_sql_media = """CREATE TABLE media(
            id BIGINT AUTO_INCREMENT,
            name varchar(255) NOT NULL UNIQUE,
            description  varchar(255),
            PRIMARY KEY (id)     
)"""

simple_sql_stage = """CREATE TABLE stage(
            id BIGINT AUTO_INCREMENT,
            name varchar(255) NOT NULL UNIQUE,
            description  varchar(255),
            PRIMARY KEY (id)       
)"""

simple_sql_category = """CREATE TABLE category(
            id BIGINT AUTO_INCREMENT, 
            name varchar(20) NOT NULL UNIQUE,
            description varchar(255),
            PRIMARY KEY (id)
)"""

simple_sql_client = """CREATE TABLE client(
            id BIGINT AUTO_INCREMENT, 
            name varchar(255) NOT NULL UNIQUE,
            description varchar (255),
            PRIMARY KEY (id)
)"""


sql_variety = """CREATE TABLE variety(
            id BIGINT AUTO_INCREMENT,
            variety_code varchar(255) NOT NULL UNIQUE,  
            name varchar(255) NOT NULL,
            description varchar(255), 
            category_id BIGINT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (category_id) REFERENCES category(id)
)"""


sql_client_order = """CREATE TABLE client_order (
            id BIGINT AUTO_INCREMENT,
            client_id  BIGINT NOT NULL,
            variety_id BIGINT NOT NULL,
            amount INT ,
            creation_date date NOT NULL DEFAULT(CURRENT_TIME()),
            shipping_date date NOT NULL,
            PRIMARY KEY (id), 
            FOREIGN KEY (client_id) REFERENCES client(id),
            FOREIGN KEY (variety_id) REFERENCES variety(id)
)"""

sql_produce_record = """CREATE TABLE produce_record(
            id varchar(255),
            variety_id BIGINT not null,
            media_id BIGINT not null,
            employee_id BIGINT not null,
            stage_id BIGINT not null,
            produce_date date NOT NULL DEFAULT(CURRENT_TIME()),
            produce_time datetime NOT NULL DEFAULT(CURRENT_TIME()),
            mother_produce_id varchar(255),
            in_stock BOOL NOT NULL,
            consumed_date date ,
            consumed_reason varchar(255) ,
            PRIMARY KEY (id),
            FOREIGN KEY(variety_id) REFERENCES variety(id),
            FOREIGN KEY(media_id) REFERENCES  media(id),
            FOREIGN KEY(employee_id) REFERENCES  staff(id),
            FOREIGN KEY(stage_id) REFERENCES  stage(id),
            FOREIGN KEY (mother_produce_id) REFERENCES  produce_record(id)
)"""


create_table(simple_sql_authorization_level)
create_table(simple_sql_category)
create_table(simple_sql_client)
create_table(simple_sql_media)
create_table(simple_sql_stage)
create_table(sql_staff)
create_table(sql_variety)
create_table(sql_client_order)
create_table(sql_produce_record)

