from .base import BaseORMTestCase
from ...models import Bookmark


class TestManager(BaseORMTestCase):
    def test_without_deleted(self):
        Bookmark.objects.filter(url='https://ru.inshaker.com/cocktails/1098-aperol-shprits').delete()

        bookmarks_without_deleted_titles = Bookmark.objects.without_deleted().values_list('title', flat=True)

        self.assertNotIn(
            'Апероль шприц. Состав, проверенный рецепт и фото коктейля Апероль шприц — Inshaker',
            bookmarks_without_deleted_titles
        )
