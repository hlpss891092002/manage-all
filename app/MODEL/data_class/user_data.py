from pydantic import BaseModel

class sign_in_data(BaseModel):
	employee_id: str
	password: str