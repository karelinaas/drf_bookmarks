from django.http import Http404
from django.shortcuts import get_object_or_404

from .base import BaseORMTestCase
from ...models import Bookmark


class TestSelect(BaseORMTestCase):
    def test_all(self):
        # Выборка всех закладок из таблицы
        all_bookmarks = Bookmark.objects.all()

        # Сверим кол-во закладок
        self.assertEquals(7, len(all_bookmarks))

        # Соберём все названия закладок, сравним списки
        bookmark_titles = [bookmark.title for bookmark in all_bookmarks]
        print(bookmark_titles)
        self.assertEquals(self.BOOKMARK_TITLES, bookmark_titles)

    def test_count(self):
        self.assertEquals(7, Bookmark.objects.count())

    def test_first(self):
        # Первая запись в выборке
        all_bookmarks = Bookmark.objects.all()

        self.assertEquals(all_bookmarks.first(), all_bookmarks[0])

        # Без ORDER BY результат непредсказуем
        print(all_bookmarks.first().title)

    def test_last(self):
        # Последняя запись в выборке
        all_bookmarks = Bookmark.objects.all()

        print(all_bookmarks.query)

        self.assertEquals(all_bookmarks.last(), all_bookmarks[6])

        # Без ORDER BY результат непредсказуем
        print(all_bookmarks.last().title)

    def test_get(self):
        # По ID
        self.assertIsNotNone(Bookmark.objects.get(pk=2))
        # По другому полю - уникальность!
        self.assertIsNotNone(Bookmark.objects.get(title='Яндекс Практикум'))

    def test_get_object_or_404(self):
        # Существующая запись
        bookmark = get_object_or_404(
            Bookmark,
            title='Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
        )
        # Проверим по полю description
        self.assertEquals((
            'Торт Наполеон в домашних условиях. Вкусный рецепт приготовления с пошаговым описанием на 382 ккал, '
            'c фото и отзывами. Удобный поиск рецептов и кулинарное вдохновение на Gastronom.ru'
        ), bookmark.description)

        # Несуществующая запись, выкинет исключение
        with self.assertRaises(Http404):
            get_object_or_404(Bookmark, title='abcdef')

    def test_values(self):
        # Выборка всех названий закладок из таблицы
        bookmark_titles = Bookmark.objects.all().values('title', 'description')

        # Получим QuerySet (~~ список) из словарей
        for bm_fields_dict in bookmark_titles:
            self.assertIn(bm_fields_dict['title'], self.BOOKMARK_TITLES)
            print(bm_fields_dict['description'])

    def test_values_list(self):
        # Выборка всех названий закладок из таблицы
        bookmark_titles = Bookmark.objects.all().values_list('title', 'description')

        # Получим QuerySet (~~ список) из кортежей
        for bm_fields_tuple in bookmark_titles:
            self.assertIn(bm_fields_tuple[0], self.BOOKMARK_TITLES)

        print(bookmark_titles)

        # Получим плоский список (можно выбрать только 1 поле)
        bookmark_titles = Bookmark.objects.all().values_list('title', flat=True)
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))
        print(bookmark_titles)

    def test_order_by(self):
        # Выборка всех закладок из таблицы в упорядоченном виде
        all_bookmarks = Bookmark.objects.all().order_by('title')

        # С ORDER BY мы уже можем предположить, что получим в .first() / .last()
        self.assertEquals('Gmail', all_bookmarks.first().title)
        self.assertEquals('Яндекс Практикум', all_bookmarks.last().title)

        print(all_bookmarks)

    def test_offset_limit(self):
        # OFFSET 4, LIMIT 2
        # [offset:offset+limit]
        bookmarks = Bookmark.objects.all().order_by('title')[4:6]

        self.assertEquals(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmarks[0].title
        )
        self.assertEquals(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmarks[1].title
        )

        print(bookmarks)
