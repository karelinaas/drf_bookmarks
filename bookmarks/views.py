from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .models import Bookmark
from .serializers import BookmarkDetailSerializer, BookmarkMinimalSerializer


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Bookmark.objects.filter(time_deleted__isnull=True)
    list_serializer_class = BookmarkMinimalSerializer
    detail_serializer_class = BookmarkDetailSerializer

    # TODO сделать поиск по списку закладок (по URL, title), сортировку, пагинацию
    # filter_backends = ...
    # ordering_fields  = ...
    # ...
    # pagination_class = ...

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.detail_serializer_class

    def get_permissions(self):
        if self.action in ('get', 'list', 'create'):
            return AllowAny(),
        if self.action == 'destroy':
            return IsAdminUser(),
        return {}
