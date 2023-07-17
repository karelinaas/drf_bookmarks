from .base import BaseORMTestCase
from ...models import Bookmark, Group


class TestBulkOperations(BaseORMTestCase):
    def test_bulk_create(self):
        new_groups_data = [
            ('Картинки', 10),
            ('Нейросети онлайн', 12),
            ('Идеи для творчества', 6),
        ]

        groups_to_create = []

        for group_data in new_groups_data:
            groups_to_create.append(Group(
                name=group_data[0],
                order=group_data[1],
            ))

        Group.objects.bulk_create(groups_to_create)

        # Проверим на существование новые группы
        for group_data in new_groups_data:
            self.assertTrue(Group.objects.filter(name=group_data[0], order=group_data[1]).exists())

    def test_bulk_update(self):
        # Хотим "почистить" данные закладок:
        # - удалить get-параметры из URL,
        # - сократить названия до 30 симв. макс.,
        # - написать дефолтное описание, если его нет.

        bookmarks = Bookmark.objects.select_related('group').all()
        bookmarks_to_update = []

        for bookmark in bookmarks:
            fields_changed = False

            if '?' in bookmark.url:
                bookmark.url = bookmark.url.split('?')[0]
                fields_changed = True

            if len(bookmark.title) > 30:
                bookmark.title = f'{bookmark.title[:27]}...'
                fields_changed = True

            if not bookmark.description:
                bookmark.description = f'Закладка из группы "{bookmark.group.name}"'
                fields_changed = True

            if fields_changed:
                bookmarks_to_update.append(bookmark)

        # Кстати, для оптимизации можно было сразу выбрать только закладки, нуждающиеся в обновлении))
        # Подумайте, как =)
        self.assertEquals(5, len(bookmarks_to_update))

        Bookmark.objects.bulk_update(
            bookmarks_to_update,
            fields=('url', 'title', 'description',),
        )

        # Проверим на существование обновленные закладки
        self.assertTrue(Bookmark.objects.filter(title='Торт Наполеон в домашних ус...').exists())
        self.assertTrue(Bookmark.objects.filter(
            title='Три рецепта «Оливье»: класс...',
            description='Закладка из группы "Рецепты"',
        ).exists())
        self.assertTrue(Bookmark.objects.filter(title='Апероль шприц. Состав, пров...').exists())
        self.assertTrue(Bookmark.objects.filter(url='https://mail.google.com/mail/u/0/').exists())
        self.assertTrue(Bookmark.objects.filter(title='Обои флизелиновые Аспект Ру...').exists())
