import random

from sqlalchemy.dialects.mysql import TINYINT

from utils.Sqlalchemy.basemodel import BaseModel
from sqlalchemy import Column, BigInteger, String, ForeignKey, DATETIME, SmallInteger

from apps.user.models import UserInfo
from utils.fastapi_utils.debug.debug import DebugManager


class Permission(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class Role(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(50))
    role = Column(SmallInteger)
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class MappingRolePermission(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role = Column(BigInteger, ForeignKey(Role.id))
    permission = Column(BigInteger, ForeignKey(Permission.id))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class MappingUserRole(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user = Column(BigInteger, ForeignKey(UserInfo.id))
    role = Column(BigInteger, ForeignKey(Role.id))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class Token(BaseModel):
    id = Column(BigInteger, primary_key=True)
    token = Column(String(255), nullable=False)
    uid = Column(BigInteger, ForeignKey(UserInfo.id))
    expire_time = Column(DATETIME)
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)


class Verification(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(6))
    email = Column(String(255))
    phone = Column(String(25))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

    @classmethod
    def code_create(cls, email, phone, debugger: DebugManager=None):
        code = ''

        if email=='' and phone=='':
            raise ValueError("No email or phone captured")

        for i in range(0, 6):
            integer = str(random.randint(0, 9))
            code += integer

        if debugger and getattr(debugger, "enabled", True):
            debugger.add(cls, method="CodeCreate", code=code)

        cls.add_instance(code=code, email=email, phone=phone, debugger=debugger)

        return