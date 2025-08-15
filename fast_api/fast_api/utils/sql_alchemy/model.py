import datetime

from sqlalchemy import Column, BigInteger, Boolean, DateTime, String

from utils.sql_alchemy.connect import get_session, transactional
from utils.sql_alchemy.base_model import Base


class Company(Base):
    __tablename__ = 'company'
    company_id = Column(BigInteger, primary_key=True)  # 使用 BigInteger 并设置主键
    company_type_id = Column(BigInteger, nullable=False)
    is_delete = Column(Boolean, nullable=False, default=False)  # 使用 Boolean 类型表示 tinyint(1)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now)
    update_time = Column(DateTime, nullable=True, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    name = Column(String(50), nullable=False)


if __name__ == '__main__':
    with get_session() as session:
        obj = Company.create(session=session, company_id=7311907193371114881)
        print(obj.company_id)
        obj = Company.create(session=session, company_id=7311907193371114882)
        print(obj.company_id)

    # with transactional() as session:
    #     obj = Company.create(session=session, company_id=7311907193371114881, commit=False)
    #     print(obj.company_id)
    #     obj = Company.create(session=session, company_id=7311907193371114882, commit=False)
    #     print(obj.company_id)
    #     raise Exception('test')
    # obj = Company.objects().filter(company_id=7211903193371114881).first()
    # print(obj.company_id)

    # obj = Company.objects().filter(create_time__gte='2025-02-16 14:43:52').first()
    # 7159903292378234881
    # print(obj.company_id)
    # print(obj)
    # print(obj.name)
    # session = SessionLocal()
    # obj = session.query(Company).filter_by(company_id=7159903292378234881).first()
    # 2025-02-16 14:43:52
    # print(obj.create_time)
    # if create_time = 2025-02-16 14:43:52
    # obj = session.query(Company).filter_by(create_time='2025-02-16 14:43:52').first()
    # print(obj.name)
    # print(Company.company_id, type(Company.company_id))
    # print(getattr(Company, 'company_id'), type(getattr(Company, 'company_id')))
