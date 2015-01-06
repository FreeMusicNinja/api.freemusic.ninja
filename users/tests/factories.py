import factory
import faker

from .. import models

fake = faker.Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    name = factory.LazyAttribute(lambda o: fake.name())
    email = factory.LazyAttribute(lambda o: fake.email())
