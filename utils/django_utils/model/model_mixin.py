from django.db import models

from utils.django_utils.model.manager import NotDeletedManager
from utils.snowflake_util import SnowflakeIDGenerator


class DeleteMixin(models.Model):
    """
        带删除标记的模型Mixin
    """
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')  # 0 未删除 1 已删除
    delete_object = NotDeletedManager()

    class Meta:
        abstract = True

    def delete(self, force_delete=False, using=None, keep_parents=False):
        if force_delete:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_delete = True
            self.save()


class UpdateTimeMixin(models.Model):
    """
        更新时间
    """
    update_time = models.DateTimeField(null=True, auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True
        ordering = ["-update_time"]


class CreateTimeMixin(models.Model):
    """
        创建时间
    """
    create_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True
        ordering = ["-create_time"]


class ObjectMixin(models.Model):
    """
        带时间戳的模型Mixin
    """
    objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # 为新记录生成唯一ID
            self.pk = SnowflakeIDGenerator().generator.value
        super().save(*args, **kwargs)

    def to_dict(self, fields=None, exclude=None):
        """
        将模型实例转换为字典。

        :param include_fields: 要包含的字段列表。如果为None，则包含所有字段。
        :param exclude_fields: 要排除的字段列表。
        :return: 一个表示模型实例的字典。
        """
        data = {}
        for field in self._meta.fields:
            field_name = field.name
            # 如果指定了包含字段且当前字段不在其中，则跳过
            if fields is not None and field_name not in fields:
                continue
            # 如果指定了排除字段且当前字段在其中，则跳过
            if exclude and field_name in exclude:
                continue
            data[field_name] = getattr(self, field_name)

        return data


class DateTimeMixin(UpdateTimeMixin, CreateTimeMixin):
    """
        带时间戳的模型Mixin
    """
    create_time = models.DateTimeField(null=True, auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(null=True, auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True
        ordering = ["-create_time"]
