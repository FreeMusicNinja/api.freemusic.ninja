from unittest import TestCase

import pytest

from ..models import Artist, Hyperlink
from ..serializers import ArtistSerializer, HyperlinkSerializer


class HyperlinkSerializerTest(TestCase):

    """Tests for Hyperlink serializer."""

    def test_valid_fields(self):
        id_ = 4
        name = 'jamendo'
        display_name = "Jamendo"
        url = "http://www.jamendo.com/artist/1333"
        tracks = 42
        link = Hyperlink(id=id_, name=name, url=url, num_tracks=tracks)
        serializer = HyperlinkSerializer(link)
        assert (serializer.data == {
            'id': id_,
            'name': name,
            'display_name': display_name,
            'url': url,
            'num_tracks': tracks,
        })


class ArtistSerializerTest(TestCase):

    """Tests for Artist serializer."""

    @pytest.mark.django_db
    def test_no_links(self):
        id_ = 2
        name = "Brad Sucks"
        artist = Artist(id=id_, name=name)
        serializer = ArtistSerializer(artist)
        assert serializer.data == {'id': id_, 'name': name, 'links': []}
