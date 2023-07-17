from django.db import models
from django.db.models.functions import Concat

from .base import BaseORMTestCase
from ...models import Group, Bookmark


class TestAnnotate(BaseORMTestCase):
    def test_simple_annotate(self):
        # Составим дополнительно "поле" из значений других полей с помощью .annotate() и Value()
        groups = Group.objects.annotate(
            str_repr=Concat('name', models.Value('__'), 'order', output_field=models.CharField())
        )

        for group in groups:
            self.assertEquals(f'{group.name}__{group.order}', group.str_repr)
            print(group.str_repr)

    def test_alias(self):
        # Когда результат самого выражения не нужен,
        # но используется для фильтрации (например), используем .alias()
        groups = Group.objects.alias(
            str_repr=Concat('name', models.Value('__'), 'order', output_field=models.CharField())
        ).filter(str_repr='Важное__0')

        for group in groups:
            self.assertFalse(hasattr(group, 'str_repr'))
            print(f'{group.name}__{group.order}')

    def test_annotate(self):
        result = Group.objects.aggregate(models.Min('order'), models.Max('order'))

        groups = Group.objects.annotate(
            min_order=models.Value(result['order__min']),
            max_order=models.Value(result['order__max']),
        )

        for group in groups:
            self.assertTrue(hasattr(group, 'min_order'))
            self.assertTrue(hasattr(group, 'max_order'))
            print(f'Группа "{group.name}", №{group.order} из {group.min_order} - {group.max_order}')
