from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    password: str
    user_role: int

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str
    user_role: RoleOut

    class Config:
        from_attributes = True