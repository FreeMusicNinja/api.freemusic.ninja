from rest_framework import permissions, viewsets

from similarities.utils import get_similar
from .models import Artist
from similarities.models import UserSimilarity, KnownArtist
from .serializers import ArtistSerializer, SimilaritySerializer, KnownArtistSerializer
from bandcamp import tasks as bandcamp_tasks

MIN_TRACKS_SIGNIFICANT = 3


class ArtistViewSet(viewsets.ModelViewSet):

    """API endpoint that allows artists to be viewed or edited"""

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    limit = 100

    def order_queryset(self, qs):
        significant = qs.filter(links__num_tracks__gte=MIN_TRACKS_SIGNIFICANT)
        results = list(significant[:self.limit])
        if len(results) < self.limit:
            results.extend(qs.exclude(pk__in=significant)[:self.limit - len(results)])
        return results

    def get_queryset(self):
        name = self.request.GET.get('name', "")
        if name:
            qs = self.order_queryset(get_similar(name))
            bandcamp_tasks.check_for_cc.delay(name)
        else:
            qs = super().get_queryset()
        return qs[:self.limit]


class KnownArtistViewSet(viewsets.ModelViewSet):

    """Endpoint for users to manage a list of known artists."""

    lookup_field = 'artist'
    queryset = KnownArtist.objects.all()
    serializer_class = KnownArtistSerializer

    def get_queryset(self):
        return self.request.user.knownartist_set

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SimilarViewSet(viewsets.ModelViewSet):

    queryset = UserSimilarity.objects.all()
    serializer_class = SimilaritySerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_fields = ['cc_artist']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
