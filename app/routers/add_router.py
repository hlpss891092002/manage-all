from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from typing import Annotated, Union
from app.MODEL.data_class.request_data_class import *
from app.MODEL.data_class.response_class import *
from app.MODEL.DB_method.add_method import *
from app.MODEL.DB_method.common_method import *
from app.MODEL.DB_method.search_method import *
from app.MODEL.swagger_ui.response_example import *

from app.CONTROL.jwt_function import user_validation


router = APIRouter()


@router.get("/api/tableItem/add/{tableName}",
             tags=["Table Item"],
             responses = table_item_response_example  
             )
async def get_input_item(tableName: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        print(tableName)
        columns = get_table_columns(tableName)
        print(columns)
        columnList = []
        for column in columns:
            if column == "id":
                continue
            elif  column == "in_employment":
                continue
            elif column == "produce_date":
                continue
            elif column == "produce_time":
                continue
            elif column == "in_stock":
                continue
            elif column == "creation_date":
                continue
            columnList.append(column)
        response = {
            "data" :  columnList
        }
        return  JSONResponse(status_code=200, content=response)

    except HTTPException as e:
        raise e    
    except TypeError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")



@router.post("/api/{tableName}",
              tags=["Table Method"],
              responses=table_CUD_response_example)
async def add_data_in_table(data : Union[variety_class, authorization_class,stage_class, staff_class, media_class, produce_record_class, order_class , category_class, client_class], payload  : Annotated[dict, Depends(user_validation)], tableName : str):
    try:
        job_position = payload["job_position"]
        if (tableName =="staff" or tableName == "authorization" )and job_position != "Engineer":
            response = {
                "error": True,
                "message" : "User authorization is not enough "
            }
            return  JSONResponse(status_code=403, content=response)
        input_dict = data.dict()
        print(input_dict)
        print(tableName)
        if tableName == "authorization":
             insert_authorization(input_dict, tableName)
        elif tableName == "client_order":
            insert_client_order(input_dict, tableName)
        elif tableName == "produce_record":
            id = input_dict["id"]
            mother_produce_id = input_dict["mother_produce_id"]
            if mother_produce_id:
                    insert_produce_record(input_dict)
                    consumed_reason = input_dict["consumed_reason"]
                    consume_mother_stock(mother_produce_id, consumed_reason, in_stock = False )
            else:
                insert_produce_record(input_dict)
        elif tableName == "staff":
            insert_staff(input_dict)
        elif tableName == "variety":
            insert_variety(input_dict)
        else:
            insert_tableName_data(input_dict, tableName)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except HTTPException as e:
        raise e    
    except TypeError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")
