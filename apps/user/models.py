from sqlalchemy import Column, BigInteger, String, ForeignKey, DATETIME, DATE
from sqlalchemy.dialects.mssql import TINYINT

from utils.Sqlalchemy.basemodel import BaseModel

class UserInfo(BaseModel):
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    phone = Column(String(25))
    password = Column(String(255))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class User(BaseModel):
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    uid = Column(BigInteger, ForeignKey(UserInfo.id),nullable=False)
    username = Column(String(255))
    cate_streak = Column(BigInteger)
    cate_latest = Column(DATE)
    cate = Column(String(10))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)
