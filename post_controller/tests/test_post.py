from django.test import Client, TestCase, tag
from rest_framework import status

from .factories import PostModelFactory


class PostTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        return

    @tag("own:get-post")
    def _test_can_get_own_posts(self):
        pass

    @tag("own:get-post")
    def _test_can_get_own_post(self):
        pass

    @tag("own:delete-post")
    def _test_can_delete_own_post(self):
        pass

    @tag("create-post")
    def _test_can_create_post(self):
        pass

    @tag("own:update-post")
    def _test_can_update_own_post(self):
        pass

    @tag("another:delete-post")
    def _test_cannot_delete_another_user_post(self):
        pass

    @tag("another:update-post")
    def _test_cannot_update_another_post(self):
        pass

    @tag("invalid-post")
    def _test_cannot_get_invalid_post(self):
        pass

    @tag()
    def _test_cannot_create_post_with_invalid_data(self):
        pass
