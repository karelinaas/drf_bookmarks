from django.db import models


class BookmarkManager(models.Manager):
    def without_deleted(self):
        return self.filter(time_deleted__isnull=True)
