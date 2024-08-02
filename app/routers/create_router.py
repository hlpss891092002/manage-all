from fastapi import *
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.MODEL.data_class.insert_data_class import *
from app.MODEL.DB_method.insert_method import *
from app.CONTROL.jwt_function import user_validation


router = APIRouter()

@router.post("/api/authorization")
async def create_authorization(authorization_data: authorization_class, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        job_position, authorization = authorization_data
        return insert_authorization(job_position, authorization)
        
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/staff")
async def create_staff(staff__data: staff_class, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        id, name, email, cellphone, account, password, authorization_id = staff__data
        insert_staff(id, name, email, cellphone, account, password, authorization_id)
        return
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/media")
async def create_media(media__data: media_class, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        media_name, description = media__data
        insert_media(media_name, description)
        return 
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/stage")
async def create_stage(stage__data: stage_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        stage_name, description = stage__data
        insert_stage(stage_name, description)
        return 
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/category")
async def create_category(category__data: category_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        category, description = category__data
        insert_category(category, description)
        return
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/client")
async def create_client(client__data: client_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        name, description = client__data
        insert_client(name, description)
        return
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/variety")
async def create_variety(variety__data: variety_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        id, name, description, photo, category_id = variety__data
        insert_variety(id, name, description, photo, category_id)
        return
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/client_order")
async def create_order(order__data: order_class, payload  : Annotated[dict, Depends(user_validation)]):
    try:
        client_id, variety_id, amount, creation_date, shipping_date = order__data
        insert_order(client_id, variety_id, amount, creation_date, shipping_date)
        return
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.post("/api/produce_record")
async def create_production(authorization_data: dict, payload  : Annotated[dict, Depends(user_validation)]):
        
    try:
        id, variety_id, media_id, producer_id, stage_id, mother_produce_id = authorization_data.values()
        insert_production(id, variety_id, media_id, producer_id, stage_id, mother_produce_id ,  consumed_reason = None)
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")


