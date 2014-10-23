from rest_framework import viewsets, permissions

from similarities.utils import get_similar
from .models import Artist
from .serializers import ArtistSerializer


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

    def pre_save(self, obj):
        # set the user making a change for simple_history to track
        obj._history_user = self.request.user
