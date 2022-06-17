#Python
from uuid import UUID

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# ----------------------------------------
#                 Models
#-----------------------------------------
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

class User(UserBase):
    first_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tarea(BaseModel):
    tarea_id : UUID = Field(
        ...,
        uselist=False
    )
    title : str = Field(
        ...,
        min_length = 5,
        max_length = 45,
    )
    body_text : str = Field( uselist=False )
    status: bool = Field(default = True)

class TareaReply(Tarea):
    message: str = Field(default= 'Successful Creation!!!')