from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from similarities.utils import get_similar
from .models import Artist
from similarities.models import UserSimilarity
from .serializers import ArtistSerializer, SimilaritySerializer


class ArtistViewSet(viewsets.ModelViewSet):

    """API endpoint that allows artists to be viewed or edited"""

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        name = self.request.GET.get('name', "")
        if name:
            qs = get_similar(name)
        else:
            qs = super().get_queryset()
        return qs[:100]


class SimilarViewSet(viewsets.ModelViewSet):

    queryset = UserSimilarity.objects.all()
    serializer_class = SimilaritySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']

    def pre_save(self, obj):
        artist = get_object_or_404(Artist, pk=self.kwargs['cc_artist_pk'])
        obj.cc_artist = artist
        obj.user = self.request.user
