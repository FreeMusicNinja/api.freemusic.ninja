from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from oauth2_provider import views as oauth2_views

from artists import views
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'artists', views.ArtistViewSet)
router.register(r'users', UserViewSet)
router.register(r'similar', views.SimilarViewSet)

user_router = routers.SimpleRouter()
user_router.register(r'known-artists', views.KnownArtistViewSet)

oauth2_urls = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
]

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^users/me/', include(user_router.urls)),
    url(r'^oauth2/', include(oauth2_urls, namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/',
        'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
]
