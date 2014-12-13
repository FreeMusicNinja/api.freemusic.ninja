from celery import shared_task

from . import scrape


@shared_task
def check_for_cc(artist_name):
    band_page_url = scrape.search_for_band_page(artist_name)
    band, band_page = scrape.band_info(band_page_url)
    for album_url in band_page.get_album_urls():
        scrape.album_info(band, "{band_page}{album_path}".format(
            band_page=band_page_url,
            album_path=album_url,
        ))
check_for_cc.rate_limit = "1/m"
