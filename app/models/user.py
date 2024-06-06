from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    username: constr(strip_whitespace=True, min_length=5, max_length=20)
    # email: EmailStr
    password: constr(strip_whitespace=True, min_length=6)  # 密码最小长度

