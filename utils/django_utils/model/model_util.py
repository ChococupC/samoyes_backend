from django.core.files.storage import FileSystemStorage
from django.db import models

from utils.django_utils.model.model_mixin import DateTimeMixin, DeleteMixin, UpdateTimeMixin, CreateTimeMixin, \
    ObjectMixin


class BaseModel(DateTimeMixin, DeleteMixin, ObjectMixin):
    """
        基础模型
    """

    class Meta:
        abstract = True
        ordering = ["-create_time"]


class NoCreateModel(DeleteMixin, DateTimeMixin, ObjectMixin):
    class Meta:
        abstract = True
        ordering = ["-update_time"]


class NoDeleteModel(DateTimeMixin, ObjectMixin):
    class Meta:
        abstract = True
        ordering = ["-create_time"]


class OnlyUpdateModel(UpdateTimeMixin, ObjectMixin):
    class Meta:
        abstract = True
        ordering = ["-update_time"]
