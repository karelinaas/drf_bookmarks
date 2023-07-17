from django.db.models import F, Q

from .base import BaseORMTestCase
from ...models import Bookmark


class TestF(BaseORMTestCase):
    def test_f(self):
        bookmarks = Bookmark.objects.filter(
            ~Q(url=F('title'))
        )

        print(bookmarks.query)

        self.assertEquals(self.BOOKMARK_TITLES, list(bookmarks.values_list('title', flat=True)))
