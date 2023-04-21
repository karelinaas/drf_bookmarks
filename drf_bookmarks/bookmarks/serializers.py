import requests
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

from .helpers import BookmarkInfoHelper
from .models import Bookmark


class BookmarkMinimalSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title')


class BookmarkDetailSerializer(ModelSerializer):
    url = fields.URLField(validators=[UniqueValidator(queryset=Bookmark.objects.filter(time_deleted__isnull=True))])

    __response: requests.Response = None

    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title', 'description')
        read_only_fields = ('time_created', 'favicon', 'title', 'description')

    def validate_url(self, value):
        try:
            self.__response = requests.get(value)
            if not self.__response.ok:
                raise Exception
        except Exception:
            raise ValidationError('URL, который вы ввели, не открывается. Возможно, он не является публичным?')
        return value

    def create(self, validated_data):
        self.__response.encoding = 'utf-8'
        bookmark_data = BookmarkInfoHelper(self.__response.text, validated_data['url']).get_info()
        return Bookmark.objects.create(**bookmark_data)
