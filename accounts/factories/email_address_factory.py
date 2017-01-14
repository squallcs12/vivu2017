from allauth.account.models import EmailAddress
from factory import DjangoModelFactory
from factory.declarations import SubFactory, LazyAttribute


class EmailAddressFactory(DjangoModelFactory):
    user = SubFactory(factory='accounts.factories.user_factory.UserFactory')
    email = LazyAttribute(lambda o: o.user.email)
    verified = True

    class Meta:
        model = EmailAddress
