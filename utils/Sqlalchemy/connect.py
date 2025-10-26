from contextlib import contextmanager, asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import create_engine
from project.settings import CONNECT
# CONNECT format: "USER:PASSWORD@HOST:PORT/DATABASE"

if not CONNECT:
    raise EnvironmentError("Connection between database is not build, please check your env.")

engine = create_engine(
    f'mysql://{CONNECT}',
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

@contextmanager
def get_session(session: Session = None):
    if session is None:
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
    else:
        yield session

@contextmanager
def transactional(session: Session = None):
    """
    通用事务管理器，判断是否已有事务，如果没有则开启事务，处理提交和回滚逻辑。
    """
    with get_session(session) as session:
        # 判断是否已经在一个事务中
        if session.in_transaction():
            # 如果已经在事务中，直接使用，不再开启新事务
            yield session
        else:
            # 如果没有开启事务，则开启事务
            with session.begin():
                yield session
