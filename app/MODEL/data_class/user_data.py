from pydantic import BaseModel

class sign_in_data(BaseModel):
	account: str
	password: str