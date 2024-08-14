import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from typing import Annotated
from time import time
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

@router.get("/api/{table_name}")
async def get_media_list(page:str, payload  : Annotated[dict, Depends(user_validation)], table_name:str, condition: str):

    try :
        print(table_name)

        page = int(page)
        condition = json.loads(condition)
        print(type(condition))
        start = time()
        data = None

        data = get_data_by_tablename(condition, page, table_name)

        end = time()
        print(f"multithread time = %.2f second" % (end -start))
        return JSONResponse(status_code=200, content=data)
    except HTTPException as e:
        raise e    
    except TypeError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"{e}")
