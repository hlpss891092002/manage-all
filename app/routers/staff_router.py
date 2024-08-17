
import os
import jwt
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
       result["yesterday_produce"] = get_yesterday_produce()
      #  result["yesterday_consume"] = get_yesterday_consume()
      #  result["category_stock"] = get_category_stock()
      #  result["largest_amount"] = get_largest_amount_stock()

       
       return result

    except Exception as e:
       raise HTTPException(status_code=500, detail=f"server error {e}")