from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    disabled: bool

    class Config:
        orm_mode = True
