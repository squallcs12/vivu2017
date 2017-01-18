import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: "username{}".format(n))
    email = factory.Faker(provider='email')
    password = 'password123'
    first_name = factory.Faker(provider='first_name')
    last_name = factory.Faker(provider='last_name')

    is_superuser = True
    is_staff = True
    is_active = True

    raw_password = None

    class Meta:
        model = get_user_model()
        exclude = ('raw_password',)

    @classmethod
    def _prepare(cls, create, password=None, **kwargs):
        user = super(UserFactory, cls)._prepare(create, **kwargs)

        user.raw_password = password
        user.set_password(password)

        if create:
            user.save()

        return user
