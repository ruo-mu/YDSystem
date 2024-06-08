# 用户模块路由

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from app.models.user import User
from app.services.userService import UserService

router = APIRouter()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post('/login')
async def login(login_form: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    用户登录
    :param login_form: 登录表单
    :return <JSONResponse>: 返回token
    """
    return user_service.login(login_form)


@router.post('/register')
async def register(user: User):
    """
    用户注册
    :param user: 用户对象
    :return:
    """
    return user_service.register(user)
