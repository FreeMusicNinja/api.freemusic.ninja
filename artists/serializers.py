from django.forms import widgets
from rest_framework import serializers

from artists.models import Artist, Hyperlink
from similarities.models import UserSimilarity, GeneralArtist


class HyperlinkSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Hyperlink
        fields = ('id', 'display_name', 'name', 'url')


class SimilaritySerializer(serializers.ModelSerializer):
    other_artist = serializers.CharField()
    cc_artist = serializers.PrimaryKeyRelatedField(widget=widgets.NumberInput())

    def validate_other_artist(self, attrs, source):
        name = attrs[source]
        artist, _ = GeneralArtist.objects.get_or_create(
            normalized_name=name.upper(), defaults={'name': name})
        attrs[source] = artist
        return attrs

    class Meta:
        model = UserSimilarity
        exclude = ('user',)


class ArtistSerializer(serializers.ModelSerializer):

    links = HyperlinkSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'links')
