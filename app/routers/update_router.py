from fastapi import *
from fastapi.responses import  JSONResponse


router = APIRouter()

@router.post("/users/", tags=["users"])
async def read_users():
    pass


@router.get("/users/me", tags=["users"])
async def read_user_me():
    pass