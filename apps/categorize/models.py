from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, DATE, DATETIME
from sqlalchemy.dialects.mysql import TINYINT

from utils.Sqlalchemy.basemodel import BaseModel

class Unit(BaseModel):
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class Category(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    unit = Column(BigInteger, ForeignKey(Unit.id), nullable=False)
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class Word(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category = Column(BigInteger, ForeignKey(Category.id), nullable=False)
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)

class CategorizeDaily(BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(DATE)
    word = Column(BigInteger, ForeignKey(Word.id), nullable=False)
    category = Column(BigInteger, ForeignKey(Category.id), nullable=False)
    position = Column(Integer)
    name = Column(String(255))
    update_time = Column(DATETIME, onupdate=True)
    create_time = Column(DATETIME)
    is_delete = Column(TINYINT,default=0)
