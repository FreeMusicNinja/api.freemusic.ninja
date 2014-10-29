from django.core.management.base import BaseCommand
from echonest.models import SimilarResponse

from ...models import GeneralArtist
from ...utils import add_new_similarities


class Command(BaseCommand):
    help = "Reprocess similarity weight values for echonest response data."

    def handle(self, *args, **options):
        responses = SimilarResponse.objects.all()
        for response in responses:
            artist = GeneralArtist.objects.get(normalized_name=response.name.upper())
            self.stdout.write("Processing: {}".format(artist.name))
            add_new_similarities(artist)
