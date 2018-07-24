from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone

UserModel = get_user_model()


class BaseModelQuerySet(QuerySet):
    def delete(self):
        return super(BaseModelQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(BaseModelQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class BaseModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(BaseModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return BaseModelQuerySet(self.model).filter(deleted_at=None)
        return BaseModelQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def delete(self):
        return self.get_queryset().update(deleted_at=timezone.now())



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()


class Institution(BaseModel):
    name = models.CharField(max_length=128)
    owner = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Campus(BaseModel):
    name = models.CharField(max_length=128)
    institution = models.ForeignKey(Institution, null=True,
                                    on_delete=models.SET_NULL)
    admin = models.OneToOneField(UserModel, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'campuses'

    def __str__(self):  
        return self.name