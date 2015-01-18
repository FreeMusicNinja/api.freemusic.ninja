from rest_framework import serializers, validators

from artists.models import Artist, Hyperlink
from similarities.models import UserSimilarity, GeneralArtist, KnownArtist


class HyperlinkSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Hyperlink
        fields = ('id', 'display_name', 'name', 'url', 'num_tracks')


class SimilaritySerializer(serializers.ModelSerializer):
    other_artist = serializers.CharField()
    cc_artist = serializers.PrimaryKeyRelatedField(style={'input_type': "number"},
                                                   queryset=Artist.objects.all())
    weight = serializers.IntegerField(default=0)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    def validate_other_artist(self, value):
        artist, _ = GeneralArtist.objects.get_or_create(
            normalized_name=value.upper(), defaults={'name': value})
        return artist

    def to_representation(self, instance):
        d = super().to_representation(instance)
        d.pop('user')
        return d

    class Meta:
        model = UserSimilarity
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


class KnownArtistSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True, source='artist')
    name = serializers.SlugRelatedField(slug_field='name', source='artist',
                                        queryset=GeneralArtist.objects.all())
    url = serializers.HyperlinkedRelatedField(read_only=True, source='artist',
                                              view_name='artist-detail')
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = KnownArtist
        exclude = ('artist', 'created', 'id', 'modified', 'user')
        validators = (
            validators.UniqueTogetherValidator(
                queryset=KnownArtist.objects.all(),
                fields=('user', 'artist'),
            ),
        )

    def to_representation(self, instance):
        d = super().to_representation(instance)
        d.pop('user')
        return d
