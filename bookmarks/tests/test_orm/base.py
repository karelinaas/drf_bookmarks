from django.test import TestCase

from ..utils import create_parent_model_test_data, create_test_data
from ...models import Bookmark, Group


class BaseORMTestCase(TestCase):
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
