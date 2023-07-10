from django.test import TestCase

from ..utils import create_parent_model_test_data, create_test_data
from ...models import Bookmark, Group


class BaseORMTestCase(TestCase):
    BOOKMARK_TITLES = [
        'Яндекс Практикум',
        'Моё обучение – Stepik',
        'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
        'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
        'Апероль шприц. Состав, проверенный рецепт и фото коктейля Апероль шприц — Inshaker',
        'Gmail',
        (
            'Обои флизелиновые Аспект Ру Соло белые 1.06 м 70436-14 в Санкт-Петербурге – '
            'купить по низкой цене в интернет-магазине Леруа Мерлен'
        ),
    ]

    def setUp(self) -> None:
        super().setUp()
        group_title_pk_map = create_parent_model_test_data(
            model=Group,
            filename='bookmarks/tests/resources/groups.csv',
            column_name_for_mapping='name',
        )

        create_test_data(
            model=Bookmark,
            filename='bookmarks/tests/resources/bookmarks.csv',
            foreign_key_field_name='group',
            parent_data_map=group_title_pk_map,
        )
