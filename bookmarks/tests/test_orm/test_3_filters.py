from datetime import date, datetime

from django.shortcuts import get_list_or_404

from bookmarks.models import Bookmark, Group
from bookmarks.tests.test_orm.base import BaseORMTestCase
from django.http import Http404


class TestFilters(BaseORMTestCase):
    def test_simple_filters(self):
        # Получим группу
        group = Group.objects.filter(
            name='Рецепты',
        ).first()

        # Проверим данные
        self.assertEquals(2, group.order)

        # Получим закладку
        bookmark = Bookmark.objects.filter(
            title='Яндекс Практикум',
        ).first()

        # Проверим данные
        self.assertEquals('https://practicum.yandex.ru/profile/backend-developer/', bookmark.url)

    def test_string_filters(self):
        bookmarks = [
            Bookmark.objects.filter(title__exact='Яндекс Практикум').first(),
            Bookmark.objects.filter(title__contains='декс').first(),
            Bookmark.objects.filter(title__startswith='Яндекс').first(),
            Bookmark.objects.filter(title__endswith='кум').first(),
            Bookmark.objects.filter(title__regex=r'Я*').first(),
        ]

        for bookmark in bookmarks:
            self.assertEquals('Яндекс Практикум', bookmark.title)
            self.assertEquals('https://practicum.yandex.ru/profile/backend-developer/', bookmark.url)

        # Регистронезависимость - i

    def test_date_filters(self):
        # Возьмем сегодняшнюю дату
        today = date.today()

        # Разберем ее на "составляющие"
        year, _, week_day = today.isocalendar()
        month = today.month

        print(year, week_day, month)

        bookmark_querysets = [
            Bookmark.objects.filter(time_created__year=year),
            Bookmark.objects.filter(time_created__week_day=week_day),
            Bookmark.objects.filter(time_created__month=month),
        ]

        # Т.к. все закладки были созданы сегодня,
        # во всех случаях получим полный их список
        for bookmark_queryset in bookmark_querysets:
            self.assertEquals(7, bookmark_queryset.count(), bookmark_queryset.count())

    def test_exclude(self):
        # Получим все закладки с буквой "м" в названии
        # Исключим 'Яндекс Практикум'
        bookmark_titles = Bookmark.objects.filter(
            title__icontains='м',
        ).exclude(
            title='Яндекс Практикум',
        ).values_list('title', flat=True)

        self.assertEquals(len(bookmark_titles), 3)
        self.assertIn(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmark_titles
        )
        self.assertIn(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmark_titles
        )
        self.assertIn(
            'Обои флизелиновые Аспект Ру Соло белые 1.06 м 70436-14 в Санкт-Петербурге – '
            'купить по низкой цене в интернет-магазине Леруа Мерлен',
            bookmark_titles
        )
        self.assertNotIn('Яндекс Практикум', bookmark_titles)

    def test_less_greater_etc_filters(self):
        # Сравнение с NULL
        bookmark = Bookmark.objects.filter(title__isnull=True)
        bookmark_titles = Bookmark.objects.filter(title__isnull=False).values_list('title', flat=True)

        # Закладок без названия нет
        self.assertEquals(0, bookmark.count())
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))

        # Больше
        group_names = Group.objects.filter(order__gt=3).values_list('name', flat=True)
        self.assertEquals(['Ремонт'], list(group_names))

        # Больше или равно
        group_names = Group.objects.filter(order__gte=3).values_list('name', flat=True)
        for title in ('Полезное', 'Ремонт'):
            self.assertIn(title, group_names)

        # Меньше
        group_names = Group.objects.filter(order__lt=3).values_list('name', flat=True)
        for title in ('Важное', 'Учёба', 'Рецепты'):
            self.assertIn(title, group_names)

        # Меньше или равно
        bookmarks = Bookmark.objects.filter(
            time_created__lte=datetime.now(),
        ).values_list('title', flat=True)
        self.assertEquals(7, bookmarks.count())

        # Вхождение в множество
        group_names = Group.objects.filter(order__in=[2, 3, 4]).values_list('name', flat=True)
        for title in ('Полезное', 'Рецепты'):
            self.assertIn(title, group_names)

        # Вхождение в диапазон
        group_names = Group.objects.filter(order__range=[0, 1]).values_list('name', flat=True)
        for title in ('Важное', 'Учёба'):
            self.assertIn(title, group_names)

    def test_many_filters(self):
        # Вот здесь будет результат
        self.assertEquals(1, Group.objects.filter(
            name='Важное',
            order=0,
        ).count())

        # А здесь - нет
        self.assertEquals(0, Group.objects.filter(
            name='Важное',
            order=2,
        ).count())

    def test_get_list_or_404(self):
        # Несуществующая выборка, выкинет исключение
        with self.assertRaises(Http404):
            get_list_or_404(Bookmark, time_created__gt=datetime.now())

    def test_exists(self):
        # Проверка, вернет ли запрос хотя бы 1 результат
        # Не возвращает модель или queryset
        self.assertTrue(Group.objects.filter(name='Важное').exists())
