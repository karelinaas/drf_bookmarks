from django.db import models

from .base import BaseORMTestCase
from ...models import Bookmark, Group


class TestRelations(BaseORMTestCase):
    GROUP_BOOKMARKS_COUNT_MAP = {
        'Учёба': 2,
        'Рецепты': 3,
        'Полезное': 0,
        'Важное': 1,
        'Ремонт': 1,
    }

    def test_bookmarks_groups(self):
        bookmark = Bookmark.objects.get(pk=1)

        self.assertEquals(1, bookmark.group.id)

    def test_groups_bookmarks(self):
        group = Group.objects.get(pk=1)

        bookmark_titles = group.bookmarks.all().values_list('title', flat=True)

        self.assertIn('Яндекс Практикум', bookmark_titles)
        self.assertIn('Моё обучение – Stepik', bookmark_titles)

    def test_filter_related(self):
        # Можно фильтровать связанные модели
        group = Group.objects.get(pk=1)

        bookmark_titles = group.bookmarks.filter(title__startswith='Я').values_list('title', flat=True)

        self.assertIn('Яндекс Практикум', bookmark_titles)
        # (а также упорядочивать и т. д.)

    def test_filter_by_related_fields(self):
        # Можно фильтровать выборку по полям связанных моделей
        bookmark_titles = Bookmark.objects.filter(
            group__name__in=['Полезное', 'Важное']
        ).values_list('title', flat=True)

        self.assertIn('Gmail', bookmark_titles)

    def test_relations_f(self):
        bookmarks = Bookmark.objects.annotate(
            group_title=models.F('group__name')
        )

        for bookmark in bookmarks:
            self.assertIn(bookmark.group_title, self.GROUP_BOOKMARKS_COUNT_MAP.keys())
            print(bookmark.group_title)
        # Полученное поле также можно использовать для фильтрации, сортировки и др.

    def test_agregate_related(self):
        # Посчитаем кол-во закладок в каждой группе
        groups = Group.objects.annotate(bookmarks_cnt=models.Count('bookmarks'))

        print(groups.query)

        for group in groups:
            bookmarks_count = self.GROUP_BOOKMARKS_COUNT_MAP[group.name]
            self.assertEquals(bookmarks_count, group.bookmarks_cnt)

    def test_prefetch_related(self):
        # Посчитаем кол-во запросов в БД при подтягивании модели по связям
        groups = Group.objects.all()
        queries = [str(groups.query)]

        for group in groups:
            queries.append(str(group.bookmarks.all().query))

        # Итого 6, 1 на выборку всех групп, +5 на выборку закладок из каждой группы
        # Проблема N + 1
        print(queries)
        self.assertEquals(6, len(queries))

        # С prefetch_related кол-во запросов будет тем же, НО
        # вместо обращения к БД каждый раз при вызове закладки
        # будет обращение к закешированному QuerySet закладок
        Group.objects.prefetch_related('bookmarks').all()

    def test_select_related(self):
        bookmarks = Bookmark.objects.select_related('group').all()

        print(bookmarks.query)

        self.assertIn('LEFT OUTER JOIN', str(bookmarks.query))

    def test_filtered_prefetch(self):
        # Выберем все группы и только те их закладки, которые содержат '.ru' в url
        groups = Group.objects.prefetch_related(
            models.Prefetch(
                lookup='bookmarks',
                queryset=Bookmark.objects.filter(url__contains='.ru'),
                to_attr='ru_bookmarks',
            )
        ).all()

        # Соберем полученные bookmark title
        bookmark_titles = []
        for group in groups:
            for bookmark in group.ru_bookmarks:
                bookmark_titles.append(bookmark.title)

        # Проверим, что мы получили только нужные данные
        for title in [
            'Яндекс Практикум',
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            (
                'Обои флизелиновые Аспект Ру Соло белые 1.06 м 70436-14 в Санкт-Петербурге – '
                'купить по низкой цене в интернет-магазине Леруа Мерлен'
            ),
        ]:
            self.assertIn(title, bookmark_titles)
