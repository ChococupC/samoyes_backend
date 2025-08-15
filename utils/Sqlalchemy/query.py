from unittest import skipIf

from sqlalchemy import desc, Function, or_

class QuerySet:

    def __init__(self, model, session):
        self.model = model
        self.query = session.query(self.model)
        self.session = session

    def _clone(self):
        new_query = QuerySet(self.model, self.session)
        new_query.query = self.query
        return new_query

    def filter(self, **kwargs) -> "QuerySet":
        filters = []
        op_and = []
        op_or = []
        new_query = self._clone()

        for key, value in kwargs.items():
            logic_op_selected = op_and

            if value == "" or value is None:
                continue

            if key.startswith("or__"):
                key = key[4:]
                logic_op_selected = op_or

            if '__' in key:
                op, attr = key.split('__')
            else:
                op, attr = 'eq', key
            if op == 'eq':
                logic_op_selected.append(getattr(self.model, attr) == value)
            elif op == 'gt':
                logic_op_selected.append(getattr(self.model, attr) > value)
            elif op == 'gte':
                logic_op_selected.append(getattr(self.model, attr) >= value)
            elif op == 'lt':
                logic_op_selected.append(getattr(self.model, attr) < value)
            elif op == 'lte':
                logic_op_selected.append(getattr(self.model, attr) <= value)
            elif op == 'in':
                logic_op_selected.append(getattr(self.model, attr).in_(
                    value if isinstance(value, (list, tuple, set)) else [value]))
            elif op == 'ex':
                logic_op_selected.append(getattr(self.model, attr) != value)
            else:
                raise ValueError(f"Invalid operator '{op}' in key '{key}'")

        if op_or:
            filters.append(or_(*op_or))

        filters.extend(op_and)

        new_query.query = new_query.query.filter(*filters)

        return new_query

    def all(self):
        return self.query.all()

    def first(self):
        return self.query.first()

    def get(self, **kwargs):
        return self.query.filter(**kwargs).one_or_none()

    def count(self):
        return self.query.count()

    def update(self, **kwargs):
        self.query.update(kwargs)
        self.session.commit()
        return self.first()

    def delete(self):
        self.query.delete()
        self.session.commit()

    def order(self, *args) -> "QuerySet" :
        new_query = self._clone()
        for key in args:
            if key.startswith("-"):
                attr = key[1:]
                new_query.query = new_query.query.order_by(desc(getattr(self.model, attr)))
            else:
                new_query.query = new_query.query.order_by(getattr(self.model, key))
        return new_query

    def group(self, *args) -> "QuerySet" :

        def expr_entities(query):
            columns = []
            # Check all selected entities in the query
            for column in query.column_descriptions:
                expr = column.get('expr')
                if isinstance(expr, Function) and expr.name:
                    columns.append(expr)
            return columns

        new_query = self._clone()
        search = expr_entities(new_query.query)
        for key in args:
            new_query.query = new_query.query.group_by(getattr(self.model,key))
            search.append(getattr(self.model,key))
        new_query.query = new_query.query.with_entities(*search)
        return new_query

    def limit(self, n: int) -> "QuerySet":
        if type(n) != int:
            raise ValueError(f"Invalid Limit: {n}")
        new_query = self._clone()
        if n != 0:
            new_query.query = new_query.query.limit(n)
        return new_query

    def offset(self, n: int) -> "QuerySet":
        if type(n) != int:
            raise ValueError(f"Invalid Offset: {n}")
        new_query = self._clone()
        new_query.query = new_query.query.offset(n)
        return new_query