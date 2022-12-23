import requests
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, ValidationError

from .helpers import BookmarkInfoHelper
from .models import Bookmark


class BookmarkMinimalSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title')


class BookmarkDetailSerializer(ModelSerializer):
    time_created = fields.DateTimeField(read_only=True)
    favicon = fields.URLField(read_only=True)
    title = fields.CharField(read_only=True)
    description = fields.CharField(read_only=True)

    __response__: requests.Response = None

    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title', 'description')

    def validate_url(self, value):
        if Bookmark.objects.filter(url=value, time_deleted__isnull=True).exists():
            raise ValidationError('Закладка с таким URL уже существует.')

        try:
            self.__response__ = requests.get(value)
            if not self.__response__.ok:
                raise Exception
        except Exception:
            raise ValidationError('URL, который вы ввели, не открывается. Возможно, он не является публичным?')

        return value

    def create(self, validated_data):
        bookmark_data = BookmarkInfoHelper(self.__response__.text, validated_data['url']).get_info()
        return Bookmark.objects.create(**bookmark_data)
