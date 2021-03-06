import factory
from auth_controller import models
from django.contrib.auth.hashers import make_password
from faker import Faker

fake_data = Faker()


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser

    first_name = "Chris"
    last_name = "Griffin"
    email = fake_data.unique.email()
    password = "famiilyguy"

    @staticmethod
    def filter(**kwargs):
        return UserModelFactory._meta.model.objects.filter(**kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raw_password = kwargs["password"]
        kwargs["password"] = make_password(raw_password)

        return super()._create(model_class, *args, **kwargs)
