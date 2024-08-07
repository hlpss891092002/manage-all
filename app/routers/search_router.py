from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.CONTROL.jwt_function import user_validation
from app.MODEL.DB_method.search_method import*
from app.MODEL.DB_method.common_method import *

router = APIRouter()

@router.get("/api/search/tableItem/{table_name}")
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

@router.post("/api/search/{table_name}")
async def get_media_list(body: dict, payload  : Annotated[dict, Depends(user_validation)], table_name:str):
    try :
        data = None

        if table_name == "category":
            data = get_category_data(body)
        elif table_name == "client":
            data = get_client_data(body)
        elif table_name == "client_order":
            data = get_client_order_data(body)
        elif table_name == "media":
            data = get_media_data(body)
        elif table_name == "produce_record":
            data = get_produce_record_data_from_condition(body)
        elif table_name == "staff":
            data = get_staff_data(body)
        elif table_name == "stage":
            data = get_stage_data(body)
        elif table_name == "variety":
            data = get_variety_data(body)

        response = {
            "data" : data
        }
        return JSONResponse(status_code=200, content=response)
    except Exception  as e:
        if(isinstance(e, AttributeError)):
            raise HTTPException(status_code=500, detail=f"server error {e} ")
        elif(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e} ")
