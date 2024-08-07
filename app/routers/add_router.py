from fastapi import *
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.MODEL.data_class.request_data_class import *
from app.MODEL.data_class.response_class import *
from app.MODEL.DB_method.add_method import *
from app.MODEL.DB_method.common_method import *
from app.MODEL.DB_method.search_method import *

from app.CONTROL.jwt_function import user_validation


router = APIRouter()


@router.get("/api/add/tableItem/{table_name}")
async def get_input_item(table_name: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        print(table_name)
        columns = get_table_columns(table_name)
        print(columns)
        columnList = []
        for column in columns:
            if column == "id":
                continue
            elif column == "authorization":
                column = "job_position"
            elif  column == "in_employment":
                continue
            elif column == "manufacturing_date":
                continue
            elif column == "manufacturing_time":
                continue
            elif column == "in_stock":
                continue
            elif column == "creation_date":
                continue
            columnList.append(column)
        response = {
            "data" :  columnList
        }
        return response

    except Exception  as e:
        raise e


# @router.post("/api/add/authorization")
# async def create_authorization(authorization_data: authorization_class, payload  : Annotated[dict, Depends(user_validation)]):
#     try :
#         job_position, authorization = authorization_data
#         return insert_authorization(job_position, authorization)
        
#     except Exception  as e:
#         raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/category")
async def create_category(category__data: category_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        input_dict = category__data.dict()
        insert_category(input_dict)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/client")
async def create_client(client_data: client_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        input_dict = client_data.dict()
        insert_client(input_dict)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/client_order")
async def create_order(order__data: order_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        input_dict = order__data.dict()
        print(input_dict)
        insert_client_order(input_dict)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            print(type(e))
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/media")
async def create_media(media__data: media_class, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        input_dict = media__data.dict()
        print(input_dict)
        insert_media(input_dict)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/produce_record")
async def create_production(authorization_data: produce_record_class, payload  : Annotated[dict, Depends(user_validation)]):
    print(authorization_data)
    try:
        input_dict = authorization_data.dict()
        id = input_dict["id"]
        print(id)
        mother_produce_id = input_dict["mother_produce_id"]
        print(mother_produce_id)
        if mother_produce_id:
            if (len(get_current_stock(mother_produce_id))):
                insert_produce_record(input_dict)
                insert_current_stock(id)
                consumed_reason = input_dict["consumed_reason"]
                consume_mother_stock(mother_produce_id, consumed_reason, in_stock = False )
                return  JSONResponse(status_code=200, content=ok_message_200.dict())
            else:
                not_found =  error_message(
	                error = True,
                    message = f"{mother_produce_id} is not exist"
                )
                return JSONResponse(status_code=400, content=not_found.dict())
        else:
            if (insert_produce_record(input_dict)):
                insert_current_stock(id)
                return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/staff")
async def create_staff(staff__data: staff_class, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        input_dict = staff__data.dict()
        # print(input_dict)
        insert_staff(input_dict)
        return  JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/stage")
async def create_stage(stage__data: stage_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        input_dict = stage__data.dict()
        print(input_dict)
        insert_stage(input_dict)
        return JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/add/variety")
async def create_variety(variety__data: variety_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        input_dict = variety__data.dict()
        print(input_dict)
        insert_variety(input_dict)
        return JSONResponse(status_code=200, content=ok_message_200.dict())
    except Exception  as e:
        if(e.status_code):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"server error {e}")