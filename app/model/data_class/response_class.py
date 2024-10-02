from pydantic import BaseModel

class response_one_line_200(BaseModel):
    ok: bool

class error_message(BaseModel):
	error:bool
	message: str

ok_message_200 =  response_one_line_200(
	ok = True
)

class databaseException(Exception):
    def __init__(self, message: str):
        self.message = message