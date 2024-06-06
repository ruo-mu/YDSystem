# 用户模块路由

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.models.user import User
from app.services.userService import UserService

router = APIRouter()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post('/login')
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    return user_service.login(login_form)


@router.post('/register')
async def register(user: User):
    return user_service.register(user)

# @router.get("/protected")
# async def protected(token: str = Depends(oauth2_scheme)):
#     return user_service.protected(token)
