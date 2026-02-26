from django.db import models

class BaseQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True)

class DeletedManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).filter(is_deleted=False)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = DeletedManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title
