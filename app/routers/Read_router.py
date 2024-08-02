from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.CONTROL.jwt_function import user_validation
from app.MODEL.DB_method.search_method import*

router = APIRouter()

@router.get("/api/tableSearchItem/{table_name}")
async def get_input_item(table_name: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
                "data" :  get_table_columns(table_name)
            }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/tableAddItem/{table_name}")
async def get_input_item(table_name: str, payload  : Annotated[dict, Depends(user_validation)]):
    try :
        print(table_name)
        if table_name == "staff":
            return ["id", "name", "email", "cellphone", "account", "password", "authorization_id"]
        elif table_name == "client":
            return ["media_name", "description"]
        elif table_name == "client_order":
            pass
        elif table_name == "media":
            pass
        elif table_name == "stage":
            pass
        elif table_name == "variety'":
            pass
        elif table_name == "category":
            pass
        elif table_name == "produce_record":
            print("1")
            response = {
                "data" :  ["id", "variety", "media", "producer", "stage", "mother_produce"]
            }
            return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/variety")
async def get_variety_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_variety_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}") 

@router.get("/api/media")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_media_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}") 

@router.get("/api/stage")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_stage_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}") 

@router.get("/api/category")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_category_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/client")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_client_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/client_order")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_client_order_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/current_stock")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_current_stock_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/produce_record")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_produce_record_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

@router.get("/api/staff")
async def get_media_list(payload  : Annotated[dict, Depends(user_validation)]):
    try :
        response = {
            "data" : get_staff_data()
        }
        return response
    except Exception  as e:
        raise HTTPException(status_code=500, detail=f"server error {e}")

