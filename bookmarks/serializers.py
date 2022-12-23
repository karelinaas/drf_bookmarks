import requests
from bs4 import BeautifulSoup
from django.utils.timezone import now
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, ValidationError

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
        if Bookmark.objects.filter(url=value, time_deleted__isnull=False).exists():
            raise ValidationError('Закладка с таким URL уже существует.')

        try:
            self.__response__ = requests.get(value)
            if not self.__response__.ok:
                raise Exception
        except Exception:
            raise ValidationError('URL, который вы ввели, не открывается. Возможно, он не является публичным?')

        return value

    def create(self, validated_data):
        soup = BeautifulSoup(self.__response__.text)

        favicon = soup.find('link', rel='shortcut icon')
        title = soup.find('title')
        description = soup.find('meta', property='og:description')

        return Bookmark.objects.create(
            favicon=favicon.get('href') if favicon else None,
            url=validated_data['url'],
            title=title.text if title else f'Закладка от {now()}',
            description=description['content'] if description else None,
        )
