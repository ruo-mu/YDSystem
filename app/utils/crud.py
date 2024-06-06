# 封装数据库增删改查操作

from typing import TypeVar, Type

from pydantic import BaseModel

from app.config.dbconfig import SessionLocal, BaseDB


class CRUD:
    T = TypeVar('T', bound=BaseDB)
    F = TypeVar('F', bound=BaseModel)

    # def __init__(self, model_schema: Type[T], model: Type[F]):
    #     self.model_schema = model_schema
    #     self.model = model
    #     self.schema = SessionLocal()
    def __init__(self, model_schema: Type[T]):
        self.model_schema = model_schema
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    def create(self, obj: T) -> T | None:
        pass

    # def read_one(self, obj: F, attr: any) -> T | None:
    #     return self.schema.query(self.model_schema).filter(getattr(self.model_schema, attr) == getattr(obj, attr)).first()
    #
    def read_all(self, obj: F, attr: any) -> list[T] | None:
        return self.db.query(self.model_schema).filter(getattr(self.model_schema, attr) == getattr(obj, attr)).all()

    def update(self, obj: T) -> T:
        pass

    def delete(self, id: int) -> T:
        pass
