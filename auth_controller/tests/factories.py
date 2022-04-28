import factory
from auth_controller import models
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser

    first_name = "Chris"
    last_name = "Griffin"
    email = "chrisgriffin@gmail.com"
    password = "familyguy"

    @staticmethod
    def filter(**kwargs):
        return UserFactory._meta.model.objects.filter(**kwargs)
