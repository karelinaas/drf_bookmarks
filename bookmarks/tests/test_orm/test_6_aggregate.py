from django.db import models

from .base import BaseORMTestCase
from ...models import Group


class TestAggregate(BaseORMTestCase):
    # Здесь во всех случаях получаем словарики вида {'название_поля__название_функции': ...}

    def test_sum(self):
        result = Group.objects.aggregate(models.Sum('order'))
        self.assertEquals(11, result['order__sum'])

    def test_count(self):
        result = Group.objects.aggregate(models.Count('name'))
        self.assertEquals(5, result['name__count'])

    def test_min(self):
        result = Group.objects.aggregate(models.Min('order'))
        self.assertEquals(0, result['order__min'])

    def test_max(self):
        result = Group.objects.aggregate(models.Max('order'))
        self.assertEquals(5, result['order__max'])

    def test_avg(self):
        result = Group.objects.aggregate(models.Avg('order'))
        self.assertEquals(2.2, result['order__avg'])
