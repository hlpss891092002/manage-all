from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional, Sequence, Type, Union
from datetime import datetime

class authorization_class(BaseModel):
    job_position: str
    authorization: str
    
class staff_class(BaseModel):
    id : int
    name : str
    email : str
    cellphone : str
    account : str
    password : str
    authorization_id : int

class media_class(BaseModel):
    media_name: str
    description: str

class stage_class(BaseModel):
    stage_name: str
    description: str

class category_class(BaseModel):
    category: str
    description: str

class client_class(BaseModel):
    name: str
    description: str

class variety_class(BaseModel):
    id : str
    name : str
    description : str
    photo : str
    category_id : int

class order_class(BaseModel):
    client_id : str
    variety_id : str
    amount : int
    creation_date : datetime
    shipping_date : datetime

# class production_class(BaseModel):
#   id:str
#   variety_id : str
#   media_id : int
#   producer_id : int
#   stage_id : int
#   mother_produce_id : Union[str, None]
#   in_stock : bool 
#   consumed_reason : Union[str, None]



