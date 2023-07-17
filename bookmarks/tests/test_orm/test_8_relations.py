from unittest import TestCase


class TestRelations(TestCase):
    def test_bookmarks_groups(self):
        ...

    def test_groups_bookmarks(self):
        ...

    def test_n_plus_one_problem(self):
        ...

    def test_select_related(self):
        ...

    def test_prefetch_related(self):
        ...

    def test_filter_by_related_fields(self):
        ...


    # def test_aggregating_annotations(self):
    #     groups = Bookmark.objects.annotate(group_cnt=models.Count('group'))
    #
    #     for g in groups:
    #         print(g.group_cnt)

# agregate related, like Author.objects.annotate(total_pages=Sum("book__pages"))
# F !!!!!!!