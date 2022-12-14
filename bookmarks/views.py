from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .models import Bookmark
from .serializers import BookmarkDetailSerializer, BookmarkListSerializer


class BookmarkViewSet(CreateModelMixin,
                      RetrieveDestroyAPIView,
                      GenericViewSet):
    queryset = Bookmark.objects.filter(time_deleted__isnull=True)
    list_serializer_class = BookmarkListSerializer
    detail_serializer_class = BookmarkDetailSerializer

    # filter_backends = (OrderingFilter, DjangoFilterBackend)
    # filter_class = BookmarkFilterSet TODO см как в новом джанго
    # pagination_class = LinkHeaderPagination TODO какой??

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return self.detail_serializer_class

    def get_permissions(self):
        if self.action in ('get', 'list', 'create'):
            return AllowAny(),
        if self.action == 'destroy':
            return IsAdminUser(),
