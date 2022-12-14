from django.urls import path, include

# TODO как тут правильно-то
urlpatterns = [
    path('api/', include('bookmarks.api.v1.urls')),
]
