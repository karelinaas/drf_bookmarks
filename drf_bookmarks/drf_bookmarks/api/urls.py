from django.conf.urls import include, url


urlpatterns = [
    url('v1/', include('drf_bookmarks.api.v1.urls', namespace='v1')),
]
