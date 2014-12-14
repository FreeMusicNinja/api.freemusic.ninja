from django.http import Http404
from rest_framework import permissions, viewsets

from similarities.utils import get_similar
from .models import Artist
from similarities.models import UserSimilarity, Similarity, update_similarities
from .serializers import ArtistSerializer, SimilaritySerializer
from bandcamp import tasks as bandcamp_tasks


class ArtistViewSet(viewsets.ModelViewSet):

    """API endpoint that allows artists to be viewed or edited"""

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        name = self.request.GET.get('name', "")
        if name:
            qs = get_similar(name)
            bandcamp_tasks.check_for_cc.delay(name)
        else:
            qs = super().get_queryset()
        return qs[:100]


class SimilarViewSet(viewsets.ModelViewSet):

    queryset = UserSimilarity.objects.all()
    serializer_class = SimilaritySerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_fields = ['cc_artist']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer(self, instance=None, *args, **kwargs):
        try:
            instance = instance or self.get_object()
        except (Http404, AssertionError):
            instance = self.get_queryset().model()
        instance.user = self.request.user
        return super().get_serializer(instance, *args, **kwargs)
