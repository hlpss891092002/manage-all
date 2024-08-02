import uuid
import os
import mysql.connector
import mysql.connector.pooling
import random
import threading
import multiprocessing as mp
from DB_method.insert_method import *
from time import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv


load_dotenv()



def insert_authorization_for_test():
    insert_authorization("manager", "1")
    insert_authorization("Systems Engineer", "1")
    insert_authorization("Administrator", "2")
    insert_authorization("Operator Leader", "3")
    insert_authorization("Operator", "4")
# insert_authorization_for_test()
def insert_staffs_for_test():
    staff_name = ["a","b","c","d","e","f","g","h","i","j","k"]

    month = datetime.now().strftime('%Y%m')
    count = 0
    cellphone = "0912345678" 
    # insertStaff
    for staff in  staff_name:
        staff_id = str(month) + str(count).zfill(4)
        email = staff + "@test.com"
        authorization = 0

        if(staff == "a"):
            authorization  =  1
        elif(staff == "b"):
            authorization  =  2
        elif(staff == "c"):
            authorization  =  3
        elif(staff == "d"):
            authorization  =  4
        else:
            authorization  =  5
        insert_staff( staff, email,cellphone, staff_id, staff_id, authorization)
        count +=1
# insert_staffs_for_test()
def insert_test_base_data():
    # insert media
    insert_media("test", "for description")
    # # insert stage
    insert_stage("begin", " for begin")
    insert_stage("middle", " for middle")
    insert_stage("final", " for final")
    # insert category 
    insert_category("a", "for a")
    insert_category("b", "for b")
    insert_category("c", "for c")
    # #  insert client
    insert_client("name", "give me money")
    insert_client("name2", "give me more money")
    insert_client("name3", "give me huge money")
    # #  insert variety
    insert_variety("AAABZ001", "read_name", "description", "photo", 1)
    insert_variety("AAABZ002", "read_name2", "description2", "photo", 2)
    insert_variety("AAABZ003", "read_name3", "description3", "photo", 3)
    # # #  insert order
    today = datetime.now()
    shipping_time = (today + timedelta(days=365))
    insert_order(1, 1, 10000, shipping_time)
    insert_order(2, 2, 20000, shipping_time)
    insert_order(3, 3, 30000, shipping_time)
    insert_order(1, 2, 40000, shipping_time)
    insert_order(1, 3, 70000, shipping_time)
# insert_test_base_data()
staff_list =[3,4,5,6,7,8,9]
mother_stock_data=[]
def insert_stock_data_for_test():
    start = time()
    for staff in staff_list:
        count = 0
        while count < 10000:
            uuid1 = uuid.uuid4()
            uuid2 = uuid.uuid4()
            uuid_final = str(uuid1) + str(uuid2)
            insert_production(uuid_final, 1, 1, staff, 1)
            insert_current_stock(uuid_final)
            mother_stock_data.append(uuid_final)
            count += 1
    end = time()
    print(f"time1 = %.2f, mount = {len(mother_stock_data)}" % (end -start))
    # print(len(mother_stock_data))
sub_mother_stock_data=[]
def insert_consume_stock_data_for_test():
    start = time()
    for mother_stock in mother_stock_data:
        num = random.randint(0, 6)
        staff = staff_list[num]
        count = 0
        while count <=2 :
            uuid1 = uuid.uuid4()
            uuid2 = uuid.uuid4()
            uuid_final = str(uuid1) + str(uuid2)
            insert_production(uuid_final, 1, 1, staff, 2, mother_stock)
            insert_current_stock(uuid_final)
            consume_mother_stock(mother_stock, "consumed")
            sub_mother_stock_data.append(uuid_final)
            count +=1
    end = time()
    print(f"time2 = %.2f, mount = {len(sub_mother_stock_data)}" % (end -start))
    

def multi_threads_test():
    start = time()
    # thread1 = threading.Thread()
    insert_stock_data_for_test()
    # thread1.start()
    # thread2 = threading.Thread()
    insert_consume_stock_data_for_test()
    # thread2.start()
    end = time()
    print(f"multithread time = %.2f" % (end -start))




# insert_stock_data_for_test()
# insert_consume_stock_data_for_test()
# with ThreadPoolExecutor(max_workers=4) as executor:
#     executor.submit(insert_stock_data_for_test())
#     executor.submit(insert_consume_stock_data_for_test())
multi_threads_test()

