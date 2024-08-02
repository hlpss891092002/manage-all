from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.CONTROL.jwt_function import user_validation
from app.MODEL.DB_method.search_method import*

router = APIRouter()



@router.post("/api/search/produce_record")
async def get_media_list(body: dict, payload  : Annotated[dict, Depends(user_validation)]):
    # try :
        # print(body)
        get_produce_record_data(body)
        # response = {
        #     "data" : get_produce_record_data()
        # }
        # return response
    # except Exception  as e:
    #     raise HTTPException(status_code=500, detail=f"server error {e}")
