from django.conf.urls import include, url
from rest_framework.authtoken import views


urlpatterns = [
    url('auth', views.obtain_auth_token),
    url('bookmarks', include('bookmarks.api.v1.urls')),
]
