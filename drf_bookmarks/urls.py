from django.urls import path, include


urlpatterns = [
    path('api/', include('drf_bookmarks.api.urls')),
]
