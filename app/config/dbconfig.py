# mysql的配置文件

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import config

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://' \
                          f'{config.username}:' \
                          f'{config.password}@' \
                          f'{config.hostname}:' \
                          f'{config.port}/' \
                          f'{config.dbname}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, bind=engine)

BaseDB = declarative_base()
