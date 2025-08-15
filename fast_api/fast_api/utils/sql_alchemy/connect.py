from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from sql import Company

engine = create_engine(
    url='mysql+pymysql://root:gtd547896321.@43.137.12.100:3306/Company',
    pool_size=10,  # 池中最大连接数量
    max_overflow=20,  # 额外允许的链接
    pool_timeout=30,  # 等待连接超时时间(秒)
    pool_recycle=1800,  # 回收连接时间(秒)
    echo=False,  # 打印详细日志
)
# 管理会话，支持线程安全
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


@contextmanager
def get_session(session: Session = None) -> Session:
    if session is None:
        session = SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    else:
        yield session


@contextmanager
def transactional(session: Session = None) -> Session:
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

# session = SessionLocal()
#
# a = session.query(Company).filter_by(company_id="7159903292378234881").first()
# print(a.name)
