# 定义users表的模型

from sqlalchemy import Column, Integer, String
from app.config.dbconfig import BaseDB


class UserSchema(BaseDB):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
