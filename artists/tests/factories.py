import factory
import faker

from .. import models

fake = faker.Factory.create()


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Artist

    name = factory.LazyAttribute(lambda o: fake.sentence(nb_words=2))


class HyperlinkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Hyperlink

    artist = factory.SubFactory(ArtistFactory)
    order = 0
