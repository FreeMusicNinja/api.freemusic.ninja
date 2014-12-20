import os
import pytest
import responses

from .. import models, queries

MODULE_PATH = os.path.dirname(__file__)
FIXTURE_PATH = os.path.abspath(os.path.join(MODULE_PATH, "..", "fixtures"))


def load_fixture(filename):
    with open(os.path.join(FIXTURE_PATH, filename)) as fixture_file:
        fixture_contents = fixture_file.read()
    return fixture_contents


@pytest.mark.django_db
@responses.activate
def test_track_query():
    query_artist = models.Artist(id=3089)
    track_url = "http://freemusicarchive.org/api/get/tracks.json?api_key={}&artist_id={}"
    responses.add(responses.GET, track_url.format(queries.API_KEY, query_artist.pk),
                  body=load_fixture("6th_Sense.json"), match_querystring=True)
    queries.query_tracks(query_artist)

    artist = models.Artist.objects.latest('pk')
    assert artist.id == 3089
    assert artist.name == "6th Sense"
    assert artist.url == "http://freemusicarchive.org/music/6th_Sense/"
    assert artist.website == "http://notherground.blogspot.com"

    album = models.Album.objects.latest('pk')
    assert album.id == 2899
    assert album.title == "It's Notherground Music!!"
    assert album.url == "http://freemusicarchive.org/music/6th_Sense/Its_Notherground_Music/"
    assert album.artist == artist

    track = models.Track.objects.latest('pk')
    assert track.id == 11797
    assert track.title == "Too Complex"
    assert track.url == "http://freemusicarchive.org/music/6th_Sense/Its_Notherground_Music/Too_Complex"
    assert track.image_file == ("http://freemusicarchive.org/file/images/tracks/"
                                + "6th_Sense_-_05_-_Too_Complex_-_2009113045601543.jpg")
    assert track.artist == artist
    assert track.album == album
    assert track.license_title is None
    assert track.license_url is None
