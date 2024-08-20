
import os
import jwt
import threading
from time import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from app.CONTROL.jwt_function import user_validation
from app.MODEL.data_class.user_data import sign_in_data
from app.MODEL.data_class.response_class import error_message
from app.MODEL.DB_method.sigin_method import check_user
from app.MODEL.authorization.autho_tables import get_table_list_from_auth, show_table
from app.MODEL.DB_method.common_method import *

load_dotenv()
router = APIRouter()

@router.get("/api/staff/auth")
async def staff_validation(payload  : Annotated[dict, Depends(user_validation)]): 
    try:
       return payload
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"server error {e}")

@router.put("/api/staff/auth")
async def check_staff_exist(body: sign_in_data): 
  employee_id = body.employee_id
  password = body.password
  print(employee_id)
  staff_data =  check_user(employee_id, password )
  print(staff_data)
  if staff_data:
    employee_id, name = staff_data.values()
    payload = {
      "iss" : "manageAll",
      "employee_id" : employee_id,
      "sub" : name,
      "exp" : datetime.now() + timedelta(days=1)
    }
    token = jwt.encode(payload, os.getenv("JWTSECRET"), algorithm="HS256")
    response_token = {
      "token" : token
    }
    return response_token
  else:
    error_message_signup_fail = error_message(
				error = True,
				message = "登入失敗，帳號或密碼失敗"
			)
    return JSONResponse(status_code=400, content=error_message_signup_fail.dict())
  
@router.get("/api/staff/tables")
async def get_table_list(payload  : Annotated[dict, Depends(user_validation)]):
    try:
      #  table_list = show_table()
       employee_id = payload["employee_id"]
       tableList = []
       result = get_table_list_from_auth(employee_id)
       tableNameList = result.keys()
       for table in tableNameList:
          if result[f"{table}"]: 
             tableList.append(table)
       print(tableList)
       return tableList
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"server error {e}")
    
@router.get("/api/latest")
async def get_latest(payload  : Annotated[dict, Depends(user_validation)]):
   try:
      result = {}
      employee_id = payload["employee_id"]
      def get_count(element):
         return element["count"]
      
      def get_stage(element):
         return element["category"]
      
      def get_yesterday_produce_most_threads_limit_10():
         start = time()
         data_from_yesterday = get_yesterday_produce_most()
         data_from_yesterday.sort(key=get_count, reverse=True)
         result["yesterday_produce_most"] = data_from_yesterday[0:10]
         end = time()
         print(f"get yesterday count , time = %.2f second" % (end -start))

      def get_yesterday_consumed_category_sort():
         start = time()
         data_consume = get_yesterday_consume_by_category()
         data_consume.sort(key=get_count, reverse=True)
         result["yesterday_consume_category"] = data_consume
         end = time()
         print(f"get yesterday consumed time = %.2f second" % (end -start))

      def get_stock_category_sort():
         start = time()
         data_stock = get_category_stock()
         data_stock.sort(key=get_stage, reverse=True)
         result["stock_category"] = data_stock
         end = time()
         print(f"get stock time = %.2f second" % (end -start))

      def get_ready_stock_sort():
         start = time()
         data_stock = get_ready_stock()
         data_stock.sort(key=get_count, reverse=True)
         result["ready_stock"] = data_stock
         end = time()
         print(f"get stock time = %.2f second" % (end -start))
      #  result["category_stock"] = get_category_stock()
      #  result["largest_amount"] = get_largest_amount_stock()

      def run_threads():
         start = time()
         a = threading.Thread(target=get_yesterday_produce_most_threads_limit_10)
         b = threading.Thread(target=get_yesterday_consumed_category_sort)
         c = threading.Thread(target=get_stock_category_sort)
         d = threading.Thread(target=get_ready_stock_sort)
         a.start()
         b.start()
         c.start()
         d.start()
         a.join()
         b.join()
         c.join()
         d.join()
         end = time()
         print(f"get run threads = %.2f second" % (end -start))
         return result
         
         
      response = run_threads()
      return response
      
   except HTTPException as e:
      raise e    
   except TypeError as e:
         raise HTTPException(status_code=500, detail=f"{e}")
   except Exception as e:
         raise HTTPException(status_code=500, detail=f"{e}")
