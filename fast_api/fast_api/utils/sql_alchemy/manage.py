from contextlib import contextmanager

from sqlalchemy.orm import Session


class BaseManager:
    def __init__(self, model, session_factory):
        self.model = model
        self.session_factory = session_factory

    @contextmanager
    def get_session(self) -> Session:
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create(self, **kwargs) -> object:
        with self.get_session() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            return instance


"""
Model.objects().filter()
"""
