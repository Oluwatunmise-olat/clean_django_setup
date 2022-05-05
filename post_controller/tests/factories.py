import factory
import faker
from auth_controller.tests.factories import UserModelFactory
from common.faker.app_provider import CustomAppProvider
from post_controller import models

fake_data = faker.Faker()
fake_data.add_provider(CustomAppProvider)


class PostModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    title = fake_data.post_titles()
    is_done = True
    description = fake_data.sentence(nb_words=15)
    author = factory.SubFactory(UserModelFactory)

    @staticmethod
    def filter(*args, **kwargs):
        return PostModelFactory._meta.model.objects.filter(*args, **kwargs)
