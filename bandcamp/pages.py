from lxml import html
import requests

def text_tostring(element):
    text_string = html.tostring(element, method="text")
    return text_string.decode('unicode_escape').strip()

class Page(object):
    url = None
    text = None
    tree = None

    def __init__(self, url, html_text=None):
        self.url = url
        if html_text:
            self.populate(html_text)

    def get(self):
        self.populate(requests.get(self.url).text)

    def populate(self, html_text=None):
        if not html_text:
            html_text = requests.get(self.url).text
        self.text = html_text
        self.tree = html.fromstring(html_text)

    def text_by_selector(self, element_id):
        return text_tostring(self.tree.cssselect(element_id)[0])


class Album(Page):

    def get_title(self):
        return self.text_by_selector("#name-section .trackTitle")

    def get_art(self):
        og_image = self.tree.cssselect("meta[property='og:image']")[0]
        return og_image.get("content")

    def get_license(self):
        return self.text_by_selector("#license")
