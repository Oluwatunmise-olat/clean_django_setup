import factory
from auth_controller import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CustomUser
    
    first_name = ""
    last_name = ""
    email = ""
    password = ""
