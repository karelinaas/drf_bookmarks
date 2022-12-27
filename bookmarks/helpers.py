from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag
from django.utils.timezone import now


class BookmarkInfoHelper:
    """
    Хэлпер для работы с html-страницами: извлекает из страницы ее фавиконку, название, описание.
    """

    # параметры тэгов с фавиконкой, названием, описание
    # обычно фавиконка это тэг <link> с атрибутом rel="shortcut icon" или rel="icon"
    FAVICON_TAG_PARAMS = [
        ('link', {'rel': 'shortcut icon'}),
        ('link', {'rel': 'icon'}),
    ]

    # обычно название страницы это тэг <title>
    TITLE_TAG_PARAMS = [
        ('title', ),
    ]

    # обычно описание страницы это тэг <meta> с атрибутами name="description" или property="og:description"
    DESCRIPTION_TAG_PARAMS = [
        ('meta', {'name': 'description'}),
        ('meta', {'property': 'og:description'}),
    ]

    def __init__(self, html: str, url: str):
        self.__soup = BeautifulSoup(html, features='html.parser')
        self.__url = url

    def get_info(self) -> dict:
        return {
            'favicon': self.__get_favicon(),
            'url': self.__url,
            'title': self.__get_title(),
            'description': self.__get_description(),
        }

    def __get_favicon(self) -> Optional[str]:
        """
        Получаем фавиконку, нам нужен ее атрибут href (там ссылка на картинку).
        """
        favicon_tag = self.__get_tag(self.FAVICON_TAG_PARAMS)
        if favicon_tag:
            favicon_href = favicon_tag.get('href')

            # у фавиконки может быть относительный путь, тогда нужно приклеить к нему домен
            if favicon_href and favicon_href.find('http') == -1 and favicon_href.find('//') == -1:
                domain = urlparse(self.__url).netloc
                return f'//{domain}/{favicon_href}'

            return favicon_href

        return None

    def __get_title(self) -> str:
        """
        Получаем название страницы, нам нужно внутреннее содержимое тэга.
        Если не удастся получить, вернем заглушку.
        """
        title_tag = self.__get_tag(self.TITLE_TAG_PARAMS)
        if title_tag:
            return title_tag.text
        return f'Закладка от {now()}'

    def __get_description(self) -> Optional[str]:
        """
        Получаем описание страницы, нам нужно содержимое атрибута content.
        """
        description_tag = self.__get_tag(self.DESCRIPTION_TAG_PARAMS)
        if description_tag:
            return description_tag.get('content')
        return None

    def __get_tag(self, tag_params: list) -> Optional[Tag]:
        """
        Метод для получения любого тэга по параметрам.
        Перебирает варианты, пока не найдет тэг.
        """
        for params in tag_params:
            tag = self.__soup.find(*params)
            if tag:
                return tag
        return None
