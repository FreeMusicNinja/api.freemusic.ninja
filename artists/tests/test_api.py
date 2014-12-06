import json
from datetime import datetime
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.contrib import auth
from rest_framework import status
from rest_framework.test import APITestCase

from artists.models import Artist
from echonest.models import SimilarResponse
from similarities.models import GeneralArtist


class ArtistTest(APITestCase):

    @patch('echonest.utils.get_similar_from_api')
    def test_find_artists(self, get_similar):
        url = reverse('artist-list')
        names = ["Mike Doughty", "Jonathan Coulton"]
        response = {
            'response': {
                'status': {
                    'message': 'Success',
                    'version': '4.2',
                    'code': 0,
                },
                'artists': [
                    {'id': 'ARHE4MO1187FB4014D', 'name': 'Mike Doughty'},
                    {'id': 'ARW7K0P1187B9B5B47', 'name': 'Barenaked Ladies'},
                    {'id': 'ARXSNCN1187B9B06A3', 'name': 'Jonathan Coulton'}
                ],
            },
        }
        artists = [Artist.objects.create(name=n) for n in names]
        get_similar.return_value = SimilarResponse(
            name="They Might Be Giants",
            response=json.dumps(response),
        )
        data = {'name': "They Might Be Giants"}
        response = self.client.get(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == [
            {'id': a.id, 'name': a.name, 'links': list(a.links.all())}
            for a in artists
        ])

    def test_get_artist(self):
        artist = Artist.objects.create(name="Brad Sucks")
        url = reverse('artist-detail', args=[artist.id])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert (response.data == {
            'id': artist.id,
            'name': artist.name,
            'links': list(artist.links.all()),
        })


class SimilarTest(APITestCase):

    def setUp(self):
        User = auth.get_user_model()
        self.user = User.objects.create(name="macro", email="macro@example.com")
        self.client.force_authenticate(user=self.user)
        artist_name = "Spoon"
        self.general_artists = [GeneralArtist.objects.get_or_create(
            normalized_name=artist_name.upper(), defaults={'name': artist_name})[0]]

    def test_list_similar(self):
        artist = Artist.objects.create(name="Brad Sucks")
        similarity = artist.usersimilarity_set.create(user=self.user, other_artist=self.general_artists[0])
        self.check_retrieve_list(artist, [similarity])

    def test_create_similar(self):
        artist = Artist.objects.create(name="Brad Sucks")
        url = reverse('usersimilarity-list')
        assert self.client.post(url, data={
            'cc_artist': artist.pk,
            'other_artist': "Emerald Park",
        }, format="json").status_code == status.HTTP_201_CREATED
        self.check_retrieve_list(artist, artist.usersimilarity_set.filter(user=self.user))

    def check_retrieve_list(self, artist, similar_instances):
        url = reverse('usersimilarity-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [{
            'other_artist': str(similarity.other_artist),
            'cc_artist': artist.pk,
            'id': similarity.pk,
            'created': similarity.created,
            'modified': similarity.modified,
            'weight': similarity.weight,
        } for similarity in similar_instances]
