import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query

from exceptions import NotFoundException

# 使用 create_engine 函数指定 MySQL 数据库的连接字符串
engine = create_engine('mysql+pymysql://root:gtd547896321.@43.137.12.100:3306/news')
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_db_auto_commit():
    db = Session()
    try:
        yield db
    finally:
        db.commit()
        db.close()


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get_pk_name(cls):
        return inspect(cls).primary_key[0].name

    @classmethod
    def get_instance_by_pk(cls, pk, session=None):
        instance = session.query(cls).filter_by(**{cls.get_pk_name(): pk}).first()

        if not instance:
            raise NotFoundException("没有这个实例")

        return instance

    @classmethod
    def get_instance(cls, raise_error=True, session=None, **kwargs):
        instance = session.query(cls).filter_by(**kwargs).first()

        if raise_error:
            if not instance:
                raise NotFoundException("没有这个实例")

        return instance

    @classmethod
    def delete_by_pk(cls, pk, session=None):
        instance = cls.get_instance_by_pk(pk=pk, session=session)
        instance.delete(session=session)

    def delete(self, session=None):
        session.delete(self)
        session.commit()

    """
        模型.objects.filter()
    """

    @classmethod
    def objects(cls) -> Query:
        with get_session() as session:
            return session.query(cls)


class Company(BaseModel):
    __tablename__ = 'company'

    company_id = Column(BigInteger, primary_key=True, autoincrement=False)  # 使用 BigInteger 并设置主键
    company_type_id = Column(BigInteger, nullable=False)
    is_delete = Column(Boolean, nullable=False, default=False)  # 使用 Boolean 类型表示 tinyint(1)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now)
    update_time = Column(DateTime, nullable=True, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    name = Column(String(50), nullable=False)

    @classmethod
    def update(cls, pk, name=None, session=None):
        instance = session.query(cls).filter_by(company_id=pk).first()
        if name:
            instance.name = name
        session.commit()
        return instance


if __name__ == '__main__':
    print(Company.objects().filter_by(company_id=7159903292378234881).first().name)
    # 创建会话
    # session = Session()

    # 查询数据
    # instance = Company.get_instance_by_pk(pk=7159903292378234881, session=session)
    # print(instance.name)
    # instance
    # instance = Company.get_instance(name="测试4", session=session)
    # print(instance.name)

    # company_instance = session.query(Company).filter_by(company_id=7159903292378234881).first()
    # print(company_instance)

    # 创建
    # company_instance = Company(company_id=7159903292378234881, company_type_id=7159903292378234880, name="测试")
    # print(session.add(company_instance))
    # session.commit()

    # 改
    # company_instance.name = "测试2"
    # session.commit()

    # 删除
    # session.delete(company_instance)
    # session.commit()
