from django.core.urlresolvers import reverse
from django.test import TestCase

from . import factories

from similarities.models import GeneralArtist


class TestLicenseFilter(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('artist-list')

    def test_open_license(self):
        track = factories.TrackFactory(
            license_title="Attribution-Noncommercial-Share Alike 3.0 United States",
            license_url="http://creativecommons.org/licenses/by-nc-sa/3.0/us/",
        )
        track.artist.save()
        response = self.client.get(self.url)
        assert response.data[0]['name'] == track.artist.name

    def test_restricted_license(self):
        print(GeneralArtist.objects.all())
        track = factories.TrackFactory(
            license_title="FMA-Limited: Download Only",
            license_url="http://freemusicarchive.org/FMA_License",
        )
        track.artist.save()
        response = self.client.get(self.url)
        assert response.data == []

    def test_changed_license(self):
        track = factories.TrackFactory(
            license_title="Attribution-Noncommercial-Share Alike 3.0 United States",
            license_url="http://creativecommons.org/licenses/by-nc-sa/3.0/us/",
        )
        track.artist.save()
        type(track).objects.update(
            license_title="FMA-Limited: Download Only",
            license_url="http://freemusicarchive.org/FMA_License",
        )
        track.artist.save()
        response = self.client.get(self.url)
        assert response.data == []
