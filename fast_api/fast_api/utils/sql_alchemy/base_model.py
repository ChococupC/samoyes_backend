from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, Session

from utils.sql_alchemy.connect import get_session
from utils.sql_alchemy.query_set import QuerySet


# Base = declarative_base()
@as_declarative()
class Base:
    id = None
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def objects(cls, session: Session = None) -> QuerySet:
        """返回绑定的 QuerySet，使用 session"""
        with get_session(session=session) as session:
            return QuerySet(cls, session=session)

    @classmethod
    def create(cls, session: Session = None, commit=True, **kwargs):
        with get_session(session=session) as session:
            instance = cls(**kwargs)
            session.add(instance)
            if commit:
                session.commit()
            return instance
