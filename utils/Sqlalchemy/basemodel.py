import datetime
from utils.Sqlalchemy.connect import get_session
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from utils.Sqlalchemy.query import QuerySet
from utils.fastapi_utils.debug.debug import DebugManager

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def objects(cls, session=None):
        with get_session(session) as session:
            return QuerySet(cls, session)

    # 将instance转变为dict(mapping)
    def to_dict(self):
        result = {}
        class_ = self.__class__
        columns = inspect(class_).columns

        for column in columns:
            name = column.name
            result[name] = getattr(self,name)

        return result

    # 获取数据（单一）
    @classmethod
    def get_instance(cls, db=None, o:str =None, error=True, debugger: DebugManager=None, **kwargs):
        instance_query = cls.objects(db).filter(**kwargs, is_delete=0)
        if o:
            instance_query = instance_query.order(o)

        instance = instance_query.first()

        if getattr(debugger, "enabled", False):
            debugger.add(
                cls,
                method="GetInstance",
                status=bool(instance),
                query=instance_query.query,
                instance=instance,
                data=instance.to_dict() if instance else kwargs
            )

        if error:
            if not instance:
                if getattr(debugger, "enabled", False):
                    debugger.display()
                raise ModuleNotFoundError("instance not found")

        return instance

    # 获取主键名称
    @classmethod
    def get_instance_key_name(cls, debugger: DebugManager=None,):
        key_name = inspect(cls).primary_key[0].name

        if getattr(debugger, "enabled", False):
            debugger.add(cls,method="GetInstanceKeyName",status=bool(key_name), key_name=key_name)

        return key_name

    # 通过主键获取数据（单一）
    @classmethod
    def get_instance_by_pk(cls, pk: int, db=None, error=True, debugger: DebugManager=None):
        key_name = cls.get_instance_key_name(debugger=debugger)
        instance = cls.get_instance(
            **{key_name: pk},
            db=db,
            debugger=debugger
        )

        if getattr(debugger, "enabled", False):
            debugger.add(cls,method="GetInstanceByPk",status=bool(instance),instance=instance)

        if error:
            if not instance:
                if getattr(debugger, "enabled", False):
                    debugger.display()
                raise ModuleNotFoundError("instance not found")

        return instance

    # 通过非主键获取数据（多份）
    @classmethod
    def get_instances_all(cls, db=None, l:int =None, o:str =None, error=True, debugger: DebugManager=None, **kwargs):
        instances_query = cls.objects(db).filter(**kwargs, is_delete=0)

        if o:
            instances_query = instances_query.order(o)

        if l:
            instances_query = instances_query.limit(l)

        instances = instances_query.all()

        if getattr(debugger, "enabled", False):
            debugger.add(
                cls,
                method="GetInstancesAll",
                status=bool(instances),
                query=instances_query.query,
                instances=instances)

        if error:
            if not instances:
                if getattr(debugger, "enabled", False):
                    debugger.display()
                raise ModuleNotFoundError("instances not found, please check your conditions.")

        return instances

    # 获取最新数据（单一）
    @classmethod
    def get_latest_instance(cls, db=None, error=True, debugger: DebugManager=None):
        key_name = cls.get_instance_key_name(debugger=debugger)
        instance = cls.get_instance(db=db,o=f"-{key_name}",debugger=debugger)

        if getattr(debugger, "enabled", False):
            debugger.add(cls, method="GetLatestInstance", status=bool(instance), instance=instance)

        if error:
            if not instance:
                if getattr(debugger, "enabled", False):
                    debugger.display()
                raise ModuleNotFoundError("instance not found")

        return instance

    # 增加数据（单一）
    @classmethod
    def add_instance(cls, db=None, debugger: DebugManager=None, **kwargs):
        dt = datetime.datetime.now()
        with get_session(db) as session:
            instance = cls.get_instance(db=session, error=False, debugger=debugger, **kwargs)

            if instance:
                if getattr(debugger, "enabled", False):
                    debugger.add(
                        cls,
                        method="AddInstance",
                        status=False,
                        instance=instance,
                        data=instance.to_dict(),
                        message="Instance Already Exist"
                    )
                    debugger.display()
                raise FileExistsError(f"The instance already exist.")

            instance = cls(**kwargs)
            instance.update_time = dt
            instance.create_time = dt

            if getattr(debugger, "enabled", False):
                debugger.add(cls,method="AddInstance",instance=instance,data=instance.to_dict())

            session.add(instance)
            if not session.in_transaction():
                print("Commit")
                session.commit()
            return instance

    # 自我（Object)删除
    def delete(self, db=None, force_delete=False, debugger: DebugManager=None):
        with get_session(db) as session:
            if force_delete:
                session.delete(self)

                if getattr(debugger, "enabled", False):
                    debugger.add(
                        self.__class__,
                        method="Delete",
                        message="force delete complete")

                session.commit()
                return

            self.update(debugger=debugger, is_delete=1)

            if getattr(debugger, "enabled", False):
                debugger.add(
                    self.__class__,
                    method="Delete",
                    message="soft delete completed")

            return

    # 删除数据（单一）
    @classmethod
    def delete_instance_by_pk(cls, pk: int, db=None, force_delete=False, debugger: DebugManager=None):
        instance = cls.get_instance_by_pk(pk=pk, db=db, debugger=debugger)

        if getattr(debugger, "enabled", False):
            debugger.add(
                cls,
                method="DeleteInstanceByPk",
                status=bool(instance),
                instance=instance,
                force_delete=force_delete,
            )

        if not instance:
            if getattr(debugger, "enabled", False):
                debugger.display()
            raise ModuleNotFoundError("instance can't be deleted because it doesn't exist")

        instance.delete(force_delete=force_delete, debugger=debugger)

        return

    # 删除最新数据（单一）
    @classmethod
    def delete_instance_latest(cls, db=None, force_delete=False, debugger: DebugManager=None):
        instance = cls.get_latest_instance(db=db,error=False, debugger=debugger)

        if getattr(debugger, "enabled", False):
            debugger.add(
                cls,
                method="DeleteInstanceLatest",
                status=bool(instance),
                instance=instance,
                force_delete=force_delete,
            )

        if not instance:
            if getattr(debugger, "enabled", False):
                debugger.display()
            raise ModuleNotFoundError("instance can't be deleted because it doesn't exist")

        instance.delete(force_delete=force_delete, debug=debugger)

        return

    # 自我(Object)更新
    def update(self, db=None, debugger: DebugManager=None, **kwargs):
        with get_session(db) as session:
            for key, value in kwargs.items():
                setattr(self, key, value)
            setattr(self,"update_time",datetime.datetime.now())
            if getattr(debugger, "enabled", False):
                debugger.add(
                    self.__class__,
                    method="Update",
                    instance=self,
                    data=self.to_dict(),
                    message="update complete",
                )

            session.add(self)
            if not session.in_transaction():
                session.commit()
            return self

    # 通过主键更改数据（单一）
    @classmethod
    def update_instance_by_pk(cls, pk: int, db=None, error=True, debugger: DebugManager=None, **kwargs):
        dt = datetime.datetime.now()
        columns = [column.name for column in inspect(cls).columns]
        instance = cls.get_instance_by_pk(pk=pk, db=db, debugger=debugger)

        if getattr(debugger, "enabled", False):
            debugger.add(
                cls,
                method="UpdateInstanceByPk",
                status=bool(instance),
                instance=instance,
                data=instance.to_dict(),
            )

        for k in kwargs:
            if k not in columns:
                if error:
                    if getattr(debugger, "enabled", False):
                        debugger.add(
                            cls,
                            method="UpdateInstanceByPk",
                            status=False,
                            message=f"instance can't be updated please check attribution '{k}'",
                        )
                        debugger.display()
                    raise ModuleNotFoundError(f"instance can't be updated please check attribution '{k}'")
                return

        if error:
            if not instance:
                if getattr(debugger, "enabled", False):
                    debugger.display()
                raise ModuleNotFoundError("instance can't be updated please check primary key")

        return instance.update(**kwargs, update_time=dt, debugger=debugger)
