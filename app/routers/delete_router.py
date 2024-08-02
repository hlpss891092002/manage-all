from fastapi import *
from fastapi.responses import  JSONResponse
from typing import Annotated
from app.MODEL.DB_method.delete_method import delete_stock_data
from app.MODEL.data_class.response_class import ok_message_200
from app.CONTROL.jwt_function import user_validation


router = APIRouter()

@router.delete("/api/", tags=["users"])
async def read_users(body: dict, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        if delete_stock_data():
            return ok_message_200
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")
