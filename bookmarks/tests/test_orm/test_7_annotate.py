from django.db import models

from .base import BaseORMTestCase
from ...models import Group


class TestAnnotate(BaseORMTestCase):
    def test_annotate(self):
        result = Group.objects.aggregate(models.Sum('order'))
        self.assertEquals(11, result['order__sum'])

    def test_aggregating_annotations(self):
        ...

    # https://docs.djangoproject.com/en/4.2/topics/db/aggregation/#interaction-with-order-by
    def test_annotate_order_by(self):
        ...

    def test_distinct(self):
        ...

    def test_filters_annotate(self):
        ...
