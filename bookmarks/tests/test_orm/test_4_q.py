from django.db.models import Q

from .base import BaseORMTestCase
from ...models import Bookmark


class TestQ(BaseORMTestCase):
    def test_q_and(self):
        bookmark = Bookmark.objects.filter(
            Q(title__startswith='Торт') &
            Q(description__startswith='Торт')
        ).first()

        self.assertEquals(
            'https://www.gastronom.ru/recipe/15617/tort-napoleon-v-domashnih-uslovijah',
            bookmark.url
        )

    def test_q_or(self):
        # | - OR
        bookmark_titles = Bookmark.objects.filter(
            Q(title__startswith='Торт') |
            Q(title__contains='рецепт')
        ).values_list('title', flat=True)

        self.assertIn(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmark_titles
        )
        self.assertIn(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmark_titles
        )

    def test_q_not(self):
        # ~ - NOT
        bookmark_titles = Bookmark.objects.filter(
            ~Q(title__contains='а')
        ).values_list('title', flat=True)

        self.assertIn('Моё обучение – Stepik', bookmark_titles)
        self.assertIn('Gmail', bookmark_titles)

    def test_many_filters(self):
        # Q можно совмещать с условиями фильтрации
        bookmark = Bookmark.objects.filter(
            Q(title__startswith='Торт'),
            url='https://www.gastronom.ru/recipe/15617/tort-napoleon-v-domashnih-uslovijah',
        ).first()

        self.assertEquals(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmark.title
        )
