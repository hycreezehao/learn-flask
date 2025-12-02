from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    # EmailStr 会自动校验是否符合邮箱格式
    email: EmailStr
    
    # min_length, max_length 限制长度
    name: str = Field(..., min_length=2, max_length=255)
    
    first_name: str 
    last_name: str
    description: str
    password: str = Field(..., min_length=6, max_length=128)

    


class UserUpdateSchema(BaseModel):
    # EmailStr 会自动校验是否符合邮箱格式
    email: EmailStr | None = None
    
    # min_length, max_length 限制长度
    name: str | None = Field(None, min_length=2)
    
    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None