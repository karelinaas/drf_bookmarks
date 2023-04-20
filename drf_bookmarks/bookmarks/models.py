from django.db.models import CharField, DateTimeField, Model, Q, UniqueConstraint, URLField
from django.utils.timezone import now


class Bookmark(Model):
    time_created = DateTimeField(auto_now_add=True)
    time_deleted = DateTimeField(null=True)
    favicon = URLField(null=True)
    url = URLField(verbose_name='URL')
    title = CharField(max_length=255)
    description = CharField(null=True, max_length=255)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['url'], condition=Q(time_deleted__isnull=True), name='URL_UNIQUE_IF_NOT_DELETED')
        ]

    def delete(self, using=None, keep_parents=False):
        self.time_deleted = now()
        self.save()
