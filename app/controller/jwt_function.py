import jwt
import os
from fastapi import  Depends, HTTPException, Security, status
from fastapi.security import  OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from typing import Annotated

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",

)
def user_validation(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, os.getenv("JWTSECRET"), algorithms="HS256")
        #塞對應的權限或 權限對應的MYSQL的帳號
        yield payload
    except InvalidTokenError as e:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail=f"invalidation token : {str(e)}",
          headers={"WWW-Authenticate": "Bearer"})
