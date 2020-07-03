from sqlalchemy import Column, Integer, String

from tuck.db import Base
from tuck.modelbase import ModelBase
import hashlib


class User(Base, ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120))
    name = Column(String(120))

    required = ["username", "password"]
    optional = ["name"]

    def __init__(self, username, password):
        self.username = username
        self.password = self.__hashPW(password)

    def checkPassword(self, password):
        return self.password == self.__hashPW(password)

    def setPassword(self, password):
        self.password = self.__hashPW(password)

    def __hashPW(self, password):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), "thisismysalt".encode("utf-8"), 100000
        )

    def __repr__(self):
        return f"<User {self.username}>"
