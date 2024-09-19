from fastapi import APIRouter, Depends
from fastapi.responses import  JSONResponse
from typing import Annotated, Union
from app.model.data_class.request_data_class import *
from app.model.data_class.response_class import *
from app.model.db.add_method import *
from app.model.db.common_method import *
from app.model.db.search_method import *
from app.model.swagger_ui.response_example import *

from app.controller.jwt_function import user_validation

router = APIRouter()

@router.get("/api/tableItem/add/{tableName}",
             tags=["Table Item"],
             responses = table_item_response_example  
             )
async def get_input_item(tableName: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        columns = get_table_columns(tableName)
        columnList = []
        skip_column = ["id", "in_employment", "produce_date", "produce_time", "in_stock", "creation_date"]
        for column in columns:
            if column in skip_column:
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
async def add_data_in_table(data : Union[VARIETY, AUTHORIZATION, STAGE, STAFF, MEDIA, PRODUCE_RECORD, ORDER, CATEGORY, CLIENT], payload  : Annotated[dict, Depends(user_validation)], tableName : str):
    try:
        job_position = payload["job_position"]
        if (tableName =="staff" or tableName == "authorization" )and job_position != "Engineer":
            response = {
                "error": True,
                "message" : "User authorization is not enough "
            }
            return  JSONResponse(status_code=403, content=response)
        input_dict = data.dict()
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
