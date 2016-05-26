import factory
from faker import Faker
from social.apps.django_app.default.models import UserSocialAuth

from common.tests.factories.user_factory import UserFactory

fake = Faker()


class UserSocialAuthFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    provider = factory.Sequence(lambda n: fake.word())
    uid = factory.Sequence(lambda n: fake.word())
    extra_data = factory.Sequence(lambda n: {'n': n})

    class Meta:
        model = UserSocialAuth
