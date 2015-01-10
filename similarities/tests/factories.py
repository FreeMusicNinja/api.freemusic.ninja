import factory
import faker

from artists.tests import factories as artists_factories
from users.tests import factories as users_factories

from .. import models

fake = faker.Factory.create()


class GeneralArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.GeneralArtist

    name = factory.LazyAttribute(lambda o: fake.sentence(nb_words=2))


class SimilarityFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Similarity
        django_get_or_create = ('other_artist', 'cc_artist')

    other_artist = factory.SubFactory(GeneralArtistFactory)
    cc_artist = factory.SubFactory(artists_factories.ArtistFactory)


class UserSimilarityFactory(SimilarityFactory):
    class Meta:
        model = models.UserSimilarity

    user = factory.SubFactory(users_factories.UserFactory)
