from pydantic import BaseModel

class SIGN_IN_DATA(BaseModel):
	employee_id: str
	password: str