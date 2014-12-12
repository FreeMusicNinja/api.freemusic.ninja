from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from similarities.utils import get_similar
from .models import Artist
from similarities.models import UserSimilarity, Similarity, update_similarities
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
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']
    filter_fields = ['cc_artist']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user

    def post_save(self, obj, created=False):
        # TODO re-update old cumulative similarity if artist name changed
        cumulative_similarity, _ = Similarity.objects.get_or_create(
            other_artist=obj.other_artist,
            cc_artist=obj.cc_artist,
        )
        update_similarities([cumulative_similarity])
