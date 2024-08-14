from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.CONTROL.jwt_function import user_validation
from app.MODEL.DB_method.update_method import*
from app.MODEL.DB_method.common_method import *


router = APIRouter()

@router.get("/api/update/tableItem/{table_name}")
async def get_input_item(table_name: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        columns_list =  get_table_columns(table_name)
        item_List = []
        for column in columns_list:
            if table_name != "produce_record":
                if column == "id":
                    continue
            if column == "password":
                continue
            item_List.append(column)

        response = {
                "data" :  item_List
            }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.put("/api/{table_name}")
async def get_media_list(body: dict, payload  : Annotated[dict, Depends(user_validation)], table_name:str):
    try :
        data = None
        if table_name == "produce_record":
            update_produce_record_data(body, table_name)

        elif table_name == "client_order":
            update_client_order_data(body, table_name)

        elif table_name == "variety":
            update_variety_data(body, table_name)
        else:
            update_non_foreign_key_data(body, table_name)

        response = {
            "ok" : True
        }
        return JSONResponse(status_code=200, content=response)
    except Exception  as e:
        print(e)
        if(isinstance(e, AttributeError)):
            raise HTTPException(status_code=500, detail=f"server error {e} ")
        elif(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e} ")
