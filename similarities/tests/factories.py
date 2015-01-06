import factory
import faker

from artists.tests import factories as artists_factories
from users.tests import factories as users_factories

from .. import models

fake = faker.Factory.create()


class GeneralArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.GeneralArtist


class UserSimilarityFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.UserSimilarity

    other_artist = factory.SubFactory(GeneralArtistFactory)
    cc_artist = factory.SubFactory(artists_factories.ArtistFactory)
    user = factory.SubFactory(users_factories.UserFactory)
