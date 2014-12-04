from purl import URL
import requests
from lxml import html

from . import SEARCH_URL, pages, models

BAND_RESULT_URL_SELECTOR = ".searchresult.band .itemurl"
BAND_PAGE_ALBUM_SELECTOR = ".leftMiddleColumns li a"


def search_for_band_page(artist_name):
    url = URL(SEARCH_URL).query_param("q", artist_name)
    response = requests.get(url)
    tree = html.fromstring(response.text)
    url_element = tree.cssselect(BAND_RESULT_URL_SELECTOR)[0]
    band_url = html.tostring(url_element, method="text")
    return band_url.decode('unicode_escape').strip()


def get_album_urls_from_band(band_page_url):
    response = requests.get(band_page_url)
    tree = html.fromstring(response.text)
    anchor_elements = tree.cssselect(BAND_PAGE_ALBUM_SELECTOR)
    return [a.get("href") for a in anchor_elements]


def album_info(album_page_url):
    album, created = models.Album.objects.get_or_create(url=album_page_url)
    if not created:
        return
    album_page = pages.Album(album_page_url)
    album_page.populate()
    album.title = album_page.get_title()
    album.art = album_page.get_art()
    album.license = album_page.get_license()
    album.save()
