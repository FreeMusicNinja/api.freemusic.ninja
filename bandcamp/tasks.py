from celery import shared_task

from artists import models as artist_models

from . import scrape


@shared_task
def check_for_cc(artist_name):
    creative_commons = False
    band_page_url = scrape.search_for_band_page(artist_name)
    if not band_page_url:
        return  # no search results found
    band, band_page = scrape.band_info(band_page_url)
    for album_url in band_page.get_album_urls():
        album = scrape.album_info(band, "{band_page}{album_path}".format(
            band_page=band_page_url,
            album_path=album_url,
        ))
        if "some rights reserved" in album.license.lower():
            creative_commons = True
    if creative_commons:  # populate api result links
        artist, _ = artist_models.Artist.objects.get_or_create(name=band.name)
        artist.links.get_or_create(
            name='bandcamp', defaults={'url': band_page_url, 'order': 25})
check_for_cc.rate_limit = "1/m"
