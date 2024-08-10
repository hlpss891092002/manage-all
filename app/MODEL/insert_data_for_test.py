import uuid
import os
import mysql.connector
import mysql.connector.pooling
import random
import threading
from datetime import datetime, timedelta
from time import time
import multiprocessing as mp
from DB_method.add_method import *
from authorization.autho_tables import *
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv


load_dotenv()


table_list = ["authorization", 'category', 'client', 'client_order', 'current_stock', 'media', 'produce_record', 'staff', 'stage', 'variety']
def insert_authorization_for_test():
    insert_authorization("manager", False, True, True, True, True, True, True, True, True, True)
    insert_authorization("Systems Engineer",  True, True, True, True, True, True, True, True, True, True)
    insert_authorization("Administrator", False, True, True, True, True, True, True, False, True, True)
    insert_authorization("Operator Leader",  False, False, False, False, True, True, True, False, True, True)
    insert_authorization("Operator",  False, False, False, False, True, False, True, False, False, False)
# insert_authorization_for_test()
def insert_staffs_for_test():
    staff_name = ["a","b","c","d","e","f","g","h","i","j","k"]
    body = {}
    
    month = datetime.now().strftime('%Y%m')
    count = 0
    cellphone = "0912345678" 
    # insertStaff
    for staff in  staff_name:
        staff_id = str(month) + str(count).zfill(4)
        email = staff + "@test.com"
        authorization = 0
        if(staff == "a"):
            authorization  =  "manager"
        elif(staff == "b"):
            authorization  =  "Systems Engineer"
        elif(staff == "c"):
            authorization  =  "Administrator"
        elif(staff == "d"):
            authorization  =  "Operator Leader"
        else:
            authorization  =  "Operator"
        body["name"] = staff
        body["email"] = email
        body["cellphone"] = cellphone
        body["employee_id"] = staff_id
        body["password"] = staff_id
        body["authorization"] = authorization
        insert_staff(body)
        count +=1
# insert_staffs_for_test()
def insert_category_for_test():
    category_list = ["Phalaenopsis", "Epidendrum", "Dendrobium", "Oncidium", "Platycerium", "Alocasia","Philodendron", "Anthurium"]
    for category in category_list:
        body = {}
        body["category"] = category
        body["description"] = f"{category} for test"
        insert_category(body)
# insert_category_for_test()        
def insert_client_for_test():
    client_list = ["台蘭", "Orchid for all", "花花農場", "尼花世界", "尼豪景觀公司", "Flor beauty","Born to bloom", "Flor Grande"]
    country = ["taiwan", "nicaragua", "Argentina", "USA", "UK"]
    for client in client_list :
        num = random.randint(0, 4)
        body = {}
        body["name"] = client
        body["description"] = f"{client} in {country[num]}"
        insert_client(body)
# insert_client_for_test()
def insert_variety_for_test():
    category_list = ["Phalaenopsis", "Epidendrum", "Dendrobium", "Oncidium", "Platycerium", "Alocasia","Philodendron", "Anthurium"]
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028"]
    for variety_code in variety_code_list :
        num = random.randint(0, 7)
        body = {}
        body["variety_code"] = variety_code
        body["name"] = f"{variety_code}{num}"
        body["description"] = f"{variety_code} in {category_list[num]}"
        body["category"] = category_list[num]
        insert_variety(body)
# insert_variety_for_test()
def insert_client_order_for_test():
    client_list = ["台蘭", "Orchid for all", "花花農場", "尼花世界", "尼豪景觀公司", "Flor beauty","Born to bloom", "Flor Grande"]
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028"]
    today = datetime.now()
    for client in client_list :
        num = random.randint(0, 7)
        body = {}
        body["client"] = client
        body["variety"] = variety_code_list[num]
        body["amount"] = random.randint(1000, 6000)
        body["shipping_date"] = today + timedelta(weeks = num)
        insert_client_order(body)
# insert_client_order_for_test() 
def insert_media_for_test():
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    for media in media_list :
        num = random.randint(0, 7)
        body = {}
        body["media"] = media
        body["description"] = f"{media} for test"
        insert_media(body)
# insert_media_for_test()
def insert_stage_for_test():
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    for stage in stage_list :
        body = {}
        body["stage"] = stage
        body["description"] = f"{stage} for test"
        insert_stage(body)
# insert_stage_for_test()
counting = []
initial_list= []
def insert_initial_produce_record_for_test():
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028"]
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    for variety_code in variety_code_list:
        count = 0
        while count <= 100:
            uid = uuid.uuid4()
            num1 = random.randint(0, 7)
            num2 = random.randint(0, 6)
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 9999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = variety_code
            body["media"] = media_list[num1]
            body["producer_id"] = staff_name[num2]
            body["stage"] = "initial"
            body["mother_produce_id"] = None
            body["consumed_reason"] = None
            print(body)
            insert_produce_record(body , in_stock = True)
            insert_current_stock(id)
            initial_list.append(id)
            count += 1
            counting.append("1")            
propagation_list = []
def insert_propagation_produce_record_for_test():
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028"]
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    for initial in initial_list:
        count = 0
        while count <= 100:
            uid = uuid.uuid4()
            num1 = random.randint(0, 7)
            num2 = random.randint(0, 6)
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 9999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = variety_code_list[num1]
            body["media"] = media_list[num1]
            body["producer_id"] = staff_name[num2]
            body["stage"] = " propagation"
            body["mother_produce_id"] = initial
            body["consumed_reason"] = "consumed"
            print(body)
            insert_produce_record(body , in_stock = True)
            insert_current_stock(id)
            consume_mother_stock(initial, "consumed", in_stock = False )
            propagation_list.append(id)
            count += 1
            counting.append("1")  
grown_list = []
def insert_grown_produce_record_for_test():
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028"]
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    for propagation in propagation_list:
        count = 0
        while count <= 10:
            uid = uuid.uuid4()
            num1 = random.randint(0, 7)
            num2 = random.randint(0, 6)
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 9999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = variety_code_list[num1]
            body["media"] = media_list[num1]
            body["producer_id"] = staff_name[num2]
            body["stage"] = "grown"
            body["mother_produce_id"] = propagation
            body["consumed_reason"] = "consumed"
            print(body)
            insert_produce_record(body , in_stock = True)
            insert_current_stock(id)
            consume_mother_stock(propagation, "grown", in_stock = False )
            grown_list.append(id)
            count += 1
            counting.append("1")  



def multi_threads_test():
    start = time()
    insert_initial_produce_record_for_test()
    insert_propagation_produce_record_for_test()
    insert_grown_produce_record_for_test()
    # thread1 = threading.Thread(target=insert_initial_produce_record_for_test)
    # thread2 = threading.Thread(target=insert_propagation_produce_record_for_test)
    # thread3 = threading.Thread(target=insert_grown_produce_record_for_test)
    # thread1.start()
    # thread2.start()
    # thread3.start()
    end = time()
    print(f"multithread time = %.2f" % (end -start))
    print(f"amount {len(counting)}")

multi_threads_test()



