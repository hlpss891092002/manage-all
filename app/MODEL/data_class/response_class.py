from pydantic import BaseModel
from typing import Any, Dict, Optional, Sequence, Type, Union

class response_one_line_200(BaseModel):
    ok: bool

class error_message(BaseModel):
	error:bool
	message: str

ok_message_200 =  response_one_line_200(
	ok = True
)

