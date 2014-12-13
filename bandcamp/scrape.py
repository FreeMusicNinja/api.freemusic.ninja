from purl import URL
import requests
from lxml import html

from . import SEARCH_URL, pages, models

BAND_RESULT_URL_SELECTOR = ".searchresult.band .itemurl"


def search_for_band_page(artist_name):
    url = URL(SEARCH_URL).query_param("q", artist_name)
    response = requests.get(url)
    tree = html.fromstring(response.text)
    url_element = tree.cssselect(BAND_RESULT_URL_SELECTOR)[0]
    band_url = html.tostring(url_element, method="text")
    return band_url.decode('unicode_escape').strip()


def band_info(band_page_url):
    band, created = models.Artist.objects.get_or_create(url=band_page_url)
    band_page = pages.Band(band_page_url)
    band_page.populate()
    if not created:
        return band, band_page
    band.name = band_page.get_name()
    band.location = band_page.get_location()
    band.url = band_page_url
    band.save()
    return band, band_page


def album_info(band, album_page_url):
    if models.Album.objects.filter(url=album_page_url).exists():
        return
    album = models.Album(url=album_page_url)
    album_page = pages.Album(album_page_url)
    album_page.populate()
    album.title = album_page.get_title()
    album.artist = band
    album.art = album_page.get_art()
    album.license = album_page.get_license()
    album.save()
