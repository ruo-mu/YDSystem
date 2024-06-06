# 定义配置文件访问接口

import configparser
import os


class Config:
    __configFile = os.path.join(os.path.dirname(__file__), "config.ini")

    def __init__(self):
        c = configparser.ConfigParser()
        c.read(self.__configFile)
        # 数据库
        self.__hostname = c.get('database', 'hostname')
        self.__username = c.get('database', 'username')
        self.__password = c.get('database', 'password')
        self.__port = c.get('database', 'port')
        self.__dbname = c.get('database', 'dbname')

    @property
    def hostname(self):
        return self.__hostname

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def port(self):
        return self.__port

    @property
    def dbname(self):
        return self.__dbname


config = Config()
