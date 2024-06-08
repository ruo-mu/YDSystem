from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.config.dbconfig import SessionLocal
from app.models.user import User
from app.schema.userschema import UserSchema
from app.utils.authorize import Authorize
from app.utils.crud import CRUD
from app.utils.verify import Verify


class UserService:
    def __init__(self):
        self.db = SessionLocal()
        self.authorize = Authorize()

    def __del__(self):
        self.db.close()

    def login(self, login_form) -> JSONResponse:
        try:
            user = User(username=login_form.username, password=login_form.password)
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail="账号密码位数不足"
            )
        user_in_db = CRUD(UserSchema).read_all(UserSchema(username=user.username), 'username')[0]
        if not user_in_db and Verify().verify_password(user.password, user_in_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = self.authorize.create_access_token(user.username, 60 * 24 * 1)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=token.model_dump()
        )

    def register(self, user: User) -> bool:
        user_list = CRUD(UserSchema).read_all(UserSchema(username=user.username), 'username')
        if [user.username == _u.username for _u in user_list]:
            # 用户名已存在
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        _user = UserSchema(username=user.username, password=Verify().get_password_hash(user.password))
        try:
            self.db.add(_user)
            self.db.commit()
            self.db.refresh(_user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="注册失败!" + str(e))
        return True
