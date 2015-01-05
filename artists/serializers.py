from rest_framework import serializers

from artists.models import Artist, Hyperlink
from similarities.models import UserSimilarity, GeneralArtist


class HyperlinkSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Hyperlink
        fields = ('id', 'display_name', 'name', 'url', 'num_tracks')


class SimilaritySerializer(serializers.ModelSerializer):
    other_artist = serializers.CharField()
    cc_artist = serializers.PrimaryKeyRelatedField(style={'input_type': "number"}, queryset=Artist.objects.all())
    weight = serializers.IntegerField(default=0)

    def validate_other_artist(self, value):
        artist, _ = GeneralArtist.objects.get_or_create(
            normalized_name=value.upper(), defaults={'name': value})
        return artist

    class Meta:
        model = UserSimilarity
        exclude = ('user',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UserSimilarity.objects.all(),
                fields=('other_artist', 'cc_artist', 'user'),
            )
        ]


class ArtistSerializer(serializers.ModelSerializer):

    links = HyperlinkSerializer(read_only=True, many=True)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'links')
