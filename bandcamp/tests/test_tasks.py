import os
import pytest
import responses

from .. import models, pages, tasks

MODULE_PATH = os.path.dirname(__file__)
FIXTURE_PATH = os.path.abspath(os.path.join(MODULE_PATH, "..", "fixtures"))


def load_fixture(filename):
    with open(os.path.join(FIXTURE_PATH, filename)) as fixture_file:
        fixture_contents = fixture_file.read()
    return fixture_contents


@pytest.mark.django_db
@responses.activate
def test_bandcamp_cc_check():
    band_url = "http://bradsucks.bandcamp.com"
    album1_url = "http://bradsucks.bandcamp.com/album/guess-whos-a-mess"
    responses.add(responses.GET, "http://bandcamp.com/search?q=Brad+Sucks",
                  body=load_fixture("search_results.html"),
                  match_querystring=True)
    responses.add(responses.GET, band_url,
                  body=load_fixture("band_page.html"))
    responses.add(responses.GET, album1_url,
                  body=load_fixture("album_page1.html"))
    responses.add(responses.GET,
                  "http://bradsucks.bandcamp.com/album/out-of-it",
                  body=load_fixture("album_page2.html"))
    responses.add(responses.GET,
                  "http://bradsucks.bandcamp.com/album/i-dont-know-what-im-doing",
                  body=load_fixture("album_page3.html"))
    tasks.check_for_cc("Brad Sucks")
    artist = models.Artist.objects.get(url=band_url)
    assert artist.name == "Brad Sucks"
    assert artist.location == "Ottawa, Ontario"
    album1 = artist.album_set.get(url=album1_url)
    assert album1.title == "Guess Who's a Mess"
    assert album1.art == "http://f1.bcbits.com/img/a1582935420_2.jpg"
    assert album1.release_date == "20121102"
    assert album1.license == "all rights reserved"


def test_retrieve_sidebar_albums():
    with open(os.path.join(FIXTURE_PATH, "mollylewis.html")) as band_file:
        band_page = pages.Band("http://mollylewis.bandcamp.com/", html_text=band_file.read())
    assert "/album/thanksgiving-vs-christmas" in band_page.get_album_urls()
