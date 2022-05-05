import json

from auth_controller.tests.factories import UserModelFactory
from django.test import Client, TestCase, tag
from rest_framework import status
from rest_framework.authtoken.models import Token

from .factories import PostModelFactory


class PostTestCases(TestCase):
    def setUp(self):
        self.client = Client()

        self.post_data = {
            "title": PostModelFactory.title,
            "is_done": PostModelFactory.is_done,
            "description": PostModelFactory.description,
        }

        self.request_header = lambda auth_token: {
            "HTTP_AUTHORIZATION": f"Bearer {auth_token}",
            "content_type": "application/json",
        }

        return

    @tag("own:get-post")
    def test_can_get_own_posts(self):

        """Test given an authenticated user, can retrieve all posts related to the user"""

        user = UserModelFactory(email="est@gmail.com")

        user2 = UserModelFactory()

        PostModelFactory(author=user)
        PostModelFactory(author=user2)

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.get("/posts/", **self.request_header(auth_token))

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json_data["success"])
        self.assertTrue(len(json_data["data"]["results"]) > 0)
        self.assertEquals(json_data["data"]["results"][0]["author"], user.id)
        self.assertNotEquals(json_data["data"]["results"][0]["author"], user2.id)

    @tag("own:get-post")
    def test_can_get_own_post(self):
        """Test given an authenticated user, can retrieve single post related to the user"""

        user = UserModelFactory()

        post = PostModelFactory(author=user)

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.get(f"/posts/{post.id}", **self.request_header(auth_token))

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json_data["success"])
        self.assertNotEquals(json_data["data"], {})
        self.assertNotEquals(len(json_data["data"]), 0)
        self.assertEquals(json_data["data"]["author"], user.id)

    @tag("own:delete-post")
    def test_can_delete_own_post(self):
        """Test given an authenticated user, can delete a  post related to the user"""

        user = UserModelFactory()

        post = PostModelFactory(author=user)

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.delete(f"/posts/{post.id}", **self.request_header(auth_token))

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostModelFactory.filter(id=post.id).exists())

    @tag("create-post")
    def test_can_create_post(self):
        """Test given an authenticated user, can create a post and post is associated with the user"""

        user = UserModelFactory(email="est@gmail.com")

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.post(
            "/posts/create", self.post_data, **self.request_header(auth_token)
        )

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(json_data["success"])
        self.assertEquals(json_data["data"]["author"], user.id)
        self.assertTrue(PostModelFactory.filter(id=json_data["data"]["id"]).exists())

    @tag("own:update-post")
    def test_can_update_own_post(self):
        """Test given an authenticated user, can update own post"""

        user = UserModelFactory()

        post = PostModelFactory(author=user)

        auth_token, _ = Token.objects.get_or_create(user=user)

        data = json.dumps({"is_done": bool(not self.post_data["is_done"])})

        response = self.client.patch(
            f"/posts/{post.id}",
            data=data,
            **self.request_header(auth_token),
        )

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json_data["success"])
        self.assertNotEquals(json_data["data"]["is_done"], self.post_data["is_done"])

    @tag("another:delete-post")
    def test_cannot_delete_another_user_post(self):
        """Test given an authenticated user, cannot delete another user post"""

        user = UserModelFactory(email="est@gmail.com")
        user2 = UserModelFactory()

        post2 = PostModelFactory(author=user2)

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.delete(f"/posts/{post2.id}", **self.request_header(auth_token))

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(PostModelFactory.filter(id=post2.id).exists())
        self.assertFalse(json_data["success"])
        self.assertEquals(json_data["error_code"], 1101)

    @tag("another:update-post")
    def test_cannot_update_another_post(self):
        """Test given an authenticated user, cannot update another user post"""

        user = UserModelFactory(email="est@gmail.com")
        user2 = UserModelFactory()

        post2 = PostModelFactory(author=user2)

        auth_token, _ = Token.objects.get_or_create(user=user)

        response = self.client.patch(
            f"/posts/{post2.id}",
            json.dumps({"is_done": bool(not self.post_data["is_done"])}),
            **self.request_header(auth_token),
        )

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(json_data["success"])
        self.assertEquals(json_data["error_code"], 1101)
        self.assertEquals(
            PostModelFactory.filter(id=post2.id).get().is_done, self.post_data["is_done"]
        )

    @tag("invalid-post-id")
    def test_cannot_get_invalid_post(self):
        """Test given an authenticated user, cannot get a post with an 'invalid id'"""

        user = UserModelFactory()

        auth_token, _ = Token.objects.get_or_create(user=user)

        INVALID_ID = 100000000000000000000000

        response = self.client.get(
            f"/posts/{INVALID_ID}",
            **self.request_header(auth_token),
        )

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(json_data["success"])
        self.assertEquals(json_data["error_code"], 1103)

    @tag()
    def _test_cannot_create_post_with_invalid_data(self):
        pass
