from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional, Sequence, Type, Union, Annotated
from datetime import datetime



class authorization_class(BaseModel):
    job_position: str
    authorization: str
    
class staff_class(BaseModel):
    name : str
    email : Union[EmailStr, None]
    cellphone : Union[str, None]
    employee_id : str
    password : str
    job_position :str
    

class media_class(BaseModel):
    name: str
    description: str

class stage_class(BaseModel):
    name: str
    description: str

class category_class(BaseModel):
    category: str
    description: str

class client_class(BaseModel):
    name: str
    description: str

class variety_class(BaseModel):
    variety_code : str
    name : str
    description : str
    category : str

class order_class(BaseModel):
    client : str
    variety_code : str
    amount : int
    shipping_date: datetime
class produce_record_class(BaseModel):
  id:str
  variety_code : str
  media : str
  employee_id : str
  stage : str
  mother_produce_id : Union[str, None]
  consumed_reason : Union[str, None]

class staff_class(BaseModel):
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




