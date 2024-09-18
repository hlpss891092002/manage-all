from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.controller.jwt_function import user_validation
from app.model.db.update_method import*
from app.model.db.common_method import *
from app.model.swagger_ui.response_example import *


router = APIRouter()

@router.get("/api/tableItem/update/{tableName}",
             tags=["Table Item"],
             responses = table_item_response_example )
async def get_input_item(tableName: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        columns_list =  get_table_columns(tableName)
        item_List = []
        for column in columns_list:
            if tableName == "produce_record" or tableName == "client_order" :
                pass
            else :
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

@router.put("/api/{tableName}",
             tags=["Table Method"], 
            responses=table_CUD_response_example)
async def update_data_from_table(body: dict, payload  : Annotated[dict, Depends(user_validation)], tableName:str):
    try :
        job_position = payload["job_position"]
        if( tableName =="staff" or tableName == "authorization") and job_position != "Engineer":
            response = {
                "error": True,
                "message" : "User authorization is not enough "
            }
            return  JSONResponse(status_code=403, content=response)
        for index_value in body : 
                condition = body[index_value]
                if tableName == "produce_record":
                    update_produce_record_data(condition, tableName, index_value)

                elif tableName == "client_order":
                    update_client_order_data(condition, tableName, index_value)

                elif tableName == "variety":
                    update_variety_data(condition, tableName, index_value)
                elif tableName == "staff":
                     update_staff_data(condition, tableName, index_value)
                else:
                    update_non_foreign_key_data(condition, tableName, index_value)

        response = {
            "ok" : True
        }
        return JSONResponse(status_code=200, content=response)
    except HTTPException as e:
        raise e    
    except TypeError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")

