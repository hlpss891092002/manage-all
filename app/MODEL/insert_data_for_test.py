import uuid
import random
import threading
import multiprocessing as mp
from datetime import datetime, timedelta, date
from time import time
from db.add_method import *
from authorization.autho_tables import *

from dotenv import load_dotenv


load_dotenv()


table_list = ["authorization", 'category', 'client', 'client_order', 'media', 'produce_record', 'staff', 'stage', 'variety']
def insert_authorization_for_test():
    manager_input_dict = {
        "authorization" : False, "category": True, "client": True, "client_order": True, "job_position": "manager", "media": True, "produce_record": True, 'staff': True, "stage": True, 'variety': True
    }
    Engineer_input_dict = {
        "authorization" : True, "category": True, "client": True, "client_order": True, "job_position": "Engineer", "media": True, "produce_record": True, 'staff': True, "stage": True, 'variety': True
    }
    Administrator_input_dict = {
        "authorization" : False, "category": True, "client": True, "client_order": True, "job_position": "Administrator", "media": True, "produce_record": True, 'staff': False, "stage": True, 'variety': True
    }
    Operator_Leader_input_dict = {
        "authorization" : False, "category": True, "client": False, "client_order": False, "job_position": "Operator Leader", "media": True, "produce_record": True, 'staff': False, "stage": True, 'variety': True
    }
    Operator_input_dict = {
        "authorization" : False, "category": False, "client": False, "client_order": False, "job_position": "Operator", "media": False, "produce_record": True, 'staff': False, "stage": False, 'variety': False
    }
    insert_authorization(manager_input_dict, "authorization")
    insert_authorization(Engineer_input_dict, "authorization")
    insert_authorization(Administrator_input_dict, "authorization")
    insert_authorization(Operator_Leader_input_dict, "authorization")
    insert_authorization(Operator_input_dict, "authorization")
    # insert_authorization("manager", False, True, True, True, True, True, True, True, True)
    # insert_authorization("Systems Engineer",  True, True, True, True, True, True, True, True, True)
    # insert_authorization("Administrator", False, True, True, True, True, True, True, False, True)
    # insert_authorization("Operator Leader",  False, False, False, False, True, True, False, True,  True)
    # insert_authorization("Operator",  False, False, False, False,  False, True, False, False, False)
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
            authorization  =  "Manager"
        elif(staff == "b"):
            authorization  =  "Engineer"
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
        body["name"] = category
        body["description"] = f"{category} for test"
        insert_tableName_data(body, "category")
# insert_category_for_test()        
def insert_client_for_test():
    client_list = ["台蘭", "Orchid for all", "花花農場", "尼花世界", "尼豪景觀公司", "Flor beauty","Born to bloom", "Flor Grande"]
    country = ["taiwan", "nicaragua", "Argentina", "USA", "UK"]
    for client in client_list :
        num = random.randint(0, 4)
        body = {}
        body["name"] = client
        body["description"] = f"{client} in {country[num]}"
        insert_tableName_data(body, "client")
# insert_client_for_test()
def insert_variety_for_test():
    category_list = ["Phalaenopsis", "Epidendrum", "Dendrobium", "Oncidium", "Platycerium", "Alocasia","Philodendron", "Anthurium"]
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028","KVV044","KWK045","KVA044","ABP032","ALB022","AWS405","WAW400","UWU040","QAQ404","OAO010","QWQ104","EQD004","NHO011","NHK010","AKB001","EVA004","BAB054","NAA101","GAA009","ADP009","GPA001","GTA009"]
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
        insert_client_order(body, "client_order")
# insert_client_order_for_test() 
def insert_media_for_test():
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    for media in media_list :
        num = random.randint(0, 7)
        body = {}
        body["name"] = media
        body["description"] = f"{media} for test"
        insert_tableName_data(body, "media")
# insert_media_for_test()
def insert_stage_for_test():
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    for stage in stage_list :
        body = {}
        body["name"] = stage
        body["description"] = f"{stage} for test"
        insert_tableName_data(body, "stage")
# insert_stage_for_test()
# 

def insert_initial_produce_record_for_test(counting, initial_list, produce_date = None):
    variety_code_list = ["AAA001", "AAB002","CAA011","ZAK001","AKA020","AAZ101","ZBA087","KAG028","KVV044","KWK045","KVV044","ABP032","ALB022","AWS405","WAW400","UWU040","QAQ404","OAO010","QWQ104","EQD004","NHO011","NHK010","AKB001","EVA004","BAB054","NAA101","GAA009","ADP009","GPA001","GTA009"]
    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    
    for variety_code in variety_code_list:
        count = 0
        num1 = random.randint(0, 7)
        num2 = random.randint(0, 6)
        week_random = random.randint(-2, 2)
        today = date.today() 
        if produce_date is None:
            produce_date = today - timedelta(weeks = 28 + week_random) -timedelta(days=num1)
        else:
            pass
        rate = random.randint(0, 4)
        while count <= rate:
            uid = uuid.uuid4()
            now = datetime.now()
            media_num = random.randint(0, 1)
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 99999999)).zfill(8)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = variety_code
            body["media"] = media_list[media_num]
            body["employee_id"] = staff_name[num2]
            body["stage"] = "initial"
            body["mother_produce_id"] = None
            body["consumed_reason"] = None
            insert_produce_record_with_produce_date(body , produce_date,  in_stock = True)
 
            initial_list.append(body)
            count += 1
            counting.append("1")            

def insert_propagation_produce_record_for_test(counting, initial_list, propagation_list, produce_date = None):

    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    
    for initial_data in initial_list:
        count = 0
        num1 = random.randint(0, 7)
        num2 = random.randint(0, 6)
        today = date.today()
        if produce_date is None:
            produce_date = today - timedelta(weeks = 23) -timedelta(days=num1)
        else:
            pass
        rate = random.randint(1, 3)
        while count <= rate:
            media_num = random.randint(2, 3)
            uid = uuid.uuid4()
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 99999999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = initial_data["variety"]
            body["media"] = media_list[media_num]
            body["employee_id"] = staff_name[num2]
            body["stage"] = "propagation"
            body["mother_produce_id"] = initial_data["id"]
            body["consumed_reason"] = "consumed for propagation"
            insert_produce_record_with_produce_date(body , produce_date,  in_stock = True)
            consume_mother_stock_with_consumed_date(initial_data["id"], "consumed for propagation", produce_date, in_stock = False )
            propagation_list.append(body)
            count += 1
            counting.append("1")  

def insert_grown_produce_record_for_test(counting, propagation_list, grown_list, produce_date = None):

    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    
    for propagation_data in propagation_list:
        count = 0
        num1 = random.randint(0, 7)
        num2 = random.randint(0, 6)
        today = date.today()
        if produce_date is None:
            produce_date = today - timedelta(weeks = 19) -timedelta(days=num1)
        else:
            pass
        
        rate = random.randint(1, 3)
        while count <= rate:
            media_num = random.randint(3, 4)
            uid = uuid.uuid4()
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 99999999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = propagation_data["variety"]
            body["media"] = media_list[media_num]
            body["employee_id"] = staff_name[num2]
            body["stage"] = "grown"
            body["mother_produce_id"] = propagation_data["id"]
            body["consumed_reason"] = "consumed for propagation"
            insert_produce_record_with_produce_date(body , produce_date,  in_stock = True)
            consume_mother_stock_with_consumed_date(propagation_data["id"], "consumed for propagation", produce_date, in_stock = False )
            grown_list.append(body)
            count += 1
            counting.append("1")  

def insert_strong_produce_record_for_test(counting, grown_list, strong_list, produce_date = None):

    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    
    for grown_data in grown_list:
        count = 0
        num1 = random.randint(0, 7)
        num2 = random.randint(0, 6)
        week_random = random.randint(-2, 2)
        today = date.today()
        if produce_date is None:
            produce_date = today - timedelta(weeks = 14 +week_random ) -timedelta(days=num1)
        else:
            pass
        rate = random.randint(0, 2)
        while count <= rate:
            media_num = random.randint(4, 6)
            uid = uuid.uuid4()
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 99999999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = grown_data["variety"]
            body["media"] = media_list[media_num]
            body["employee_id"] = staff_name[num2]
            body["stage"] = "strong"
            body["mother_produce_id"] = grown_data["id"]
            body["consumed_reason"] = "consumed for propagation"
            insert_produce_record_with_produce_date(body , produce_date,  in_stock = True)
            consume_mother_stock_with_consumed_date(grown_data["id"], "consumed for propagation", produce_date, in_stock = False )
            strong_list.append(body)
            count += 1
            counting.append("1")  

def insert_rooting_produce_record_for_test(counting, strong_list, produce_date = None):

    media_list = ["IAA", "IBA", "BAA", "BBA", "MAA", "MBA", "FAA", "FBA"  ]
    staff_name = ["2024080004","2024080005","2024080006","2024080007","2024080008","2024080009","2024080010"]
    stage_list = ["initial","propagation", "grown", "strong", "rooting"]
    
    for strong_data in strong_list:
        count = 0
        num1 = random.randint(0, 7)
        num2 = random.randint(0, 6)
        week_random = random.randint(-2, 2)
        today = date.today()
        produce_date = today - timedelta(weeks = 9 + week_random) -timedelta(days=num1)
        rate = random.randint(0, 1)
        while count <= rate:
            media_num = random.randint(6, 7)
            uid = uuid.uuid4()
            now = datetime.now()
            second = now.second
            min = now.minute
            microsec = now.microsecond
            random_num =  str(random.randint(0, 99999999)).zfill(2)
            id = str(second) + str(min) + str(microsec) + random_num + str(uid)
            body= {}
            body["id"] = id
            body["variety"] = strong_data["variety"]
            body["media"] = media_list[media_num]
            body["employee_id"] = staff_name[num2]
            body["stage"] = "rooting"
            body["mother_produce_id"] = strong_data["id"]
            body["consumed_reason"] = "consumed for propagation"
            insert_produce_record_with_produce_date(body , produce_date,  in_stock = True)
            consume_mother_stock_with_consumed_date(strong_data["id"], "consumed for propagation", produce_date, in_stock = False )
            count += 1
            counting.append("1")  

def data_for_test_rooting(root_day = None):
    start = time()
    counting = []
    initial_list= []
    propagation_list = []
    grown_list = []
    strong_list = [] 
    insert_initial_produce_record_for_test(counting, initial_list, root_day)
    insert_propagation_produce_record_for_test(counting, initial_list, propagation_list)
    insert_grown_produce_record_for_test(counting, propagation_list, grown_list)
    insert_strong_produce_record_for_test(counting, grown_list, strong_list)
    insert_rooting_produce_record_for_test(counting, strong_list)
    end = time()


def data_for_test_strong(strong_day= None):
    start = time()
    counting = []
    initial_list= []
    propagation_list = []
    grown_list = []
    strong_list = [] 
    insert_initial_produce_record_for_test(counting, initial_list, strong_day)
    insert_propagation_produce_record_for_test(counting, initial_list, propagation_list)
    insert_grown_produce_record_for_test(counting, propagation_list, grown_list)
    insert_strong_produce_record_for_test(counting, grown_list, strong_list)

    end = time()

def data_for_test_grown(grown_day = None):
    start = time()
    counting = []
    initial_list= []
    propagation_list = []
    grown_list = []
    strong_list = [] 
    insert_initial_produce_record_for_test(counting, initial_list, grown_day)
    insert_propagation_produce_record_for_test(counting, initial_list, propagation_list)
    insert_grown_produce_record_for_test(counting, propagation_list, grown_list)

    end = time()


def data_for_test_propagation(propagation_day = None):
    start = time()
    counting = []
    initial_list= []
    propagation_list = []
    grown_list = []
    strong_list = [] 
    insert_initial_produce_record_for_test(counting, initial_list, propagation_day)
    insert_propagation_produce_record_for_test(counting, initial_list, propagation_list)

    end = time()


def data_for_test_initial(recent_day = None):
    start = time()
    counting = []
    initial_list= []
    propagation_list = []
    grown_list = []
    strong_list = [] 
    insert_initial_produce_record_for_test(counting, initial_list, recent_day)
    end = time()

    
def data_recent_week():
    today = date.today()
    num_random = random.randint(1, 7)
    yesterday = today - timedelta(days=1)
    day_random = today - timedelta(days=num_random)
    root_day = day_random - timedelta(weeks=21)
    strong_day = day_random - timedelta(weeks=17)
    grown_day = day_random - timedelta(weeks=13)
    propagation_day = day_random - timedelta(weeks=9)
    recent_day = today - timedelta(days=num_random)
    
    
    # data_for_test_initial(recent_day)
    data_for_test_initial(yesterday)
    data_for_test_propagation(propagation_day)
    data_for_test_grown(grown_day)
    data_for_test_strong(strong_day)
    data_for_test_rooting(root_day)

def multi_threads_test():
    start = time()
    a = threading.Thread(target=data_for_test_rooting)
    b = threading.Thread(target=data_for_test_strong)
    c = threading.Thread(target=data_for_test_grown)
    d = threading.Thread(target=data_for_test_propagation)
    e = threading.Thread(target=data_for_test_initial)
    # f = threading.Thread(target=data_recent_week)
    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    # f.start()
    a.join()
    b.join()
    c.join()
    d.join()
    e.join()
    end = time()
    print(f"multi thread time = %.2f" % (end -start))


loop_count = 0
while loop_count <= 10: 
    multi_threads_test()
    loop_count += 1 

data_recent_week()




