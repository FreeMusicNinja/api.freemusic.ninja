import factory
import faker

from .. import models

fake = faker.Factory.create()


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Artist

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda o: fake.sentence(nb_words=2))


class TrackFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Track

    id = factory.Sequence(lambda n: n + 1000)
    title = factory.LazyAttribute(lambda o: fake.sentence(nb_words=3))
    artist = factory.SubFactory(ArtistFactory)
