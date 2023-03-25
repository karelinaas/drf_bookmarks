from rest_framework import filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .models import Bookmark
from .serializers import BookmarkDetailSerializer, BookmarkMinimalSerializer


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Bookmark.objects.filter(time_deleted__isnull=True).order_by('-id')
    list_serializer_class = BookmarkMinimalSerializer
    detail_serializer_class = BookmarkDetailSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'time_created', 'url', 'title']
    search_fields = ['url', 'title']
    pagination_class = PageNumberPagination

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
