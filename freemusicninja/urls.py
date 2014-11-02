from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from artists.views import ArtistViewSet, SimilarViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'users', UserViewSet)
router.register(r'similar', SimilarViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/',
        'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
]
