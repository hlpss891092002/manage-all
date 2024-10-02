from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime

class STAFF(BaseModel):
    name : str
    email : Union[EmailStr, None]
    cellphone : Union[str, None]
    employee_id : str
    password : str
    job_position :str
    
class MEDIA(BaseModel):
    name: str
    description: str

class STAGE(BaseModel):
    name: str
    description: str

class CATEGORY(BaseModel):
    category: str
    description: str

class CLIENT(BaseModel):
    name: str
    description: str

class VARIETY(BaseModel):
    variety_code : str
    name : str
    description : str
    category : str

class ORDER(BaseModel):
    client : str
    variety_code : str
    amount : int
    shipping_date: datetime
class PRODUCE_RECORD(BaseModel):
  id:str
  variety_code : str
  media : str
  employee_id : str
  stage : str
  mother_produce_id : Union[str, None]
  consumed_reason : Union[str, None]

class AUTHORIZATION(BaseModel):
    authorization : str
    category:  str
    client : str
    client_order : str
    job_position : str
    media : str
    produce_record : str
    staff : str
    stage : str
    variety : str




