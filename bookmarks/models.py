from django.db.models import CharField, DateTimeField, Model, URLField
from django.utils.timezone import now


class Bookmark(Model):
    time_created = DateTimeField(auto_now_add=True)
    time_deleted = DateTimeField(null=True)
    favicon = URLField(null=True)
    url = URLField(unique=True)
    title = CharField(max_length=255)
    description = CharField(null=True, max_length=255)

    def delete(self, using=None, keep_parents=False):
        self.time_deleted = now()
        self.save()
