import os
import pytest
import responses

from artists import models as artists_models

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
    track_url = "http://freemusicarchive.org/api/get/tracks.json?api_key={}&artist_id={}&limit=20000"
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
    assert track.license_title == "Attribution-Noncommercial-Share Alike 3.0 United States"
    assert track.license_url == "http://creativecommons.org/licenses/by-nc-sa/3.0/us/"
    assert track.language_code == "en"
    assert track.duration == "02:26"
    assert track.number == 5
    assert track.disc_number == 1
    assert track.explicit == ""
    assert track.explicit_notes is None
    assert track.copyright_c is None
    assert track.copyright_p is None
    assert track.composer is None
    assert track.lyricist is None
    assert track.publisher is None
    assert not track.instrumental
    assert track.information is None
    assert track.date_recorded is None
    assert track.comments == 0
    assert track.favorites == 0
    assert track.listens == 335
    assert track.interest == 1213
    assert track.bit_rate == 192000
    assert track.date_created == "4/30/2009 02:29:11 PM"
    assert track.file == "music/Notherground_Music/6th_Sense/Its_Notherground_Music/6th_Sense_-_05_-_Too_Complex.mp3"
    assert track.license_image_file == "http://i.creativecommons.org/l/by-nc-sa/3.0/us/88x31.png"
    assert track.license_image_file_large == "http://fma-files.s3.amazonaws.com/resources/img/licenses/by-nc-sa.png"
    assert track.license_parent_id == 5
    assert track.tags == []
    assert set(track.genres.values_list('pk', flat=True)) == {21}

    genre = models.Genre.objects.latest('pk')
    assert genre.id == 21
    assert genre.title == "Hip-Hop"
    assert genre.url == "http://freemusicarchive.org/genre/Hip-Hop/"

    hyperlink = artists_models.Hyperlink.objects.get(artist__name=artist.name)
    assert hyperlink.url == artist.url
    assert hyperlink.order == 40
    assert hyperlink.num_tracks == 33
