from celery import shared_task

from . import scrape


@shared_task
def check_for_cc(artist_name):
    band_page_url = scrape.search_for_band_page(artist_name)
    album_urls = scrape.get_album_urls_from_band(band_page_url)
    for album_url in album_urls:
        scrape.album_info("{band_page}{album_path}".format(
            band_page=band_page_url,
            album_path=album_url,
        ))
