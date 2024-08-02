
import os
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from app.MODEL.data_class.user_data import sign_in_data
from app.MODEL.data_class.response_class import error_message
from app.MODEL.DB_method.sigin_method import check_user
from app.MODEL.authorization.autho_tables import get_table_list_from_auth
from app.CONTROL.jwt_function import user_validation

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
  account = body.account
  password = body.password
  print(account)
  staff_data =  check_user(account, password )
  print(staff_data)
  if staff_data:
    account, name = staff_data.values()
    payload = {
      "iss" : "manageAll",
      "account" : account,
      "sub" : name,
      "exp" : datetime.now() + timedelta(days=7)
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
       account = payload["account"]
       return get_table_list_from_auth(account)
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"server error {e}")