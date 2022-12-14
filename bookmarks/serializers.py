import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now
from rest_framework import fields
from rest_framework.serializers import ListSerializer, ModelSerializer

from .models import Bookmark


class BookmarkListSerializer(ListSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title')


class BookmarkDetailSerializer(ModelSerializer):
    # TODO чек, работает ли валидация урла из модели
    # TODO чек RETRIEVE c пустыми полями
    # TODO чек readonly
    time_created = fields.DateTimeField(read_only=True)
    favicon = fields.URLField(read_only=True)
    title = fields.CharField(read_only=True)
    description = fields.CharField(read_only=True)

    __response__: requests.Response = None

    class Meta:
        model = Bookmark
        fields = ('id', 'time_created', 'favicon', 'url', 'title', 'description')

    # TODO какие искл-я кидать?
    def validate_url(self, value):
        self.__response__ = requests.get(value)
        if not self.__response__.ok:
            pass  # TODO
        return value

    # TODO readonly!!!!
    # def validate(self, attrs):
    #     if attrs.keys() != ['url']:
    #         pass
    #
    #     return attrs

    def create(self, validated_data):
        soup = BeautifulSoup(self.__response__.text)

        favicon = soup.find('link', rel='shortcut icon')
        title = soup.find('title')
        description = soup.find('meta', name='description')

        Bookmark.objects.create(
            favicon=favicon.get('href') if favicon else None,
            url=validated_data['url'],
            title=title.text if title else f'Bookmark {now()}',
            description=description.text,
        )
