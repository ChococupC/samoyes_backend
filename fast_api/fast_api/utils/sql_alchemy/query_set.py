from sqlalchemy.orm import Session


class QuerySet:
    def __init__(self, model, session: Session):
        self.model = model
        self.query = session.query(self.model)
        self.session = session

    def _clone(self) -> 'QuerySet':
        new_query = QuerySet(self.model, self.session)
        new_query.query = self.query
        return new_query

    def filter(self, **kwargs) -> 'QuerySet':
        new_query = self._clone()

        for key, value in kwargs.items():
            if '__' in key:
                attr, op = key.split('__')
            else:
                attr, op = key, 'eq'

            if op == 'eq':
                new_query.query = new_query.query.filter(getattr(self.model, attr) == value)
            elif op == 'gt':
                new_query.query = new_query.query.filter(getattr(self.model, attr) > value)
            elif op == 'lt':
                new_query.query = new_query.query.filter(getattr(self.model, attr) < value)
            elif op == 'gte':
                new_query.query = new_query.query.filter(getattr(self.model, attr) >= value)
            elif op == 'lte':
                new_query.query = new_query.query.filter(getattr(self.model, attr) <= value)
            elif op == 'in':
                new_query.query = new_query.query.filter(getattr(self.model, attr).in_(value))
            else:
                raise ValueError(f"Invalid operator: {op}")

        return new_query

    def order_by(self, *order_fields: str) -> 'QuerySet':
        """排序"""
        new_query = self._clone()
        '''
            session.query(User).order_by(User.name.desc(), User.age.asc())
        '''
        order_conditions = []
        for field in order_fields:
            if field.startswith('-'):
                order_conditions.append(getattr(self.model, field[1:]).desc())
            else:
                order_conditions.append(getattr(self.model, field).asc())

        new_query.query = new_query.query.order_by(*order_conditions)
        return new_query

    def limit(self, limit: int) -> 'QuerySet':
        """限制"""
        new_query = self._clone()

        return new_query

    # def filter(self, **kwargs) -> 'QuerySet':

    #     self.query = self.query.filter_by(**kwargs)
    #     return self

    def first(self):
        return self.query.first()

    def all(self):
        return self.query.all()

    def order_by(self, *order_fields: str) -> 'QuerySet':
        """排序"""


if __name__ == '__main__':
    """
    a_filter =A.objects().filter().order_by().limit().offset()
    a_filter = a_filter.filter()
    c_filter = a_filter.filter()
    d_filter = c_filter.filter()
    """
