from email import header

from common.enums import UserTypes
from django.test import Client, TestCase, tag
from rest_framework import status

from .factories import UserFactory


class AuthenticationTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {
            "first_name": UserFactory.first_name,
            "last_name": UserFactory.last_name,
            "password": UserFactory.password,
            "email": UserFactory.email,
        }
        return

    @tag("user-signup")
    def test_user_signup_with_valid_data(self):
        """Test given valid sign up data, user is created"""

        response = self.client.post("/auth/signup", self.data)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(json_data["success"])

        with self.assertRaises(KeyError):
            json_data["error_code"]

        is_user = UserFactory.filter(email=self.data["email"])

        self.assertTrue(is_user.exists())

    @tag("user-signup")
    def test_user_signup_with_existing_email(self):
        """Test given an invalid data such as an already existing email, no user is created"""

        UserFactory()

        self.data["first_name"], self.data["last_name"] = "cool", "kid"

        response = self.client.post("/auth/signup", self.data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(json_data["success"])
        self.assertEquals(json_data["error_code"], 1304)

        is_user = UserFactory.filter(
            first_name=self.data["first_name"], last_name=self.data["last_name"]
        )

        self.assertFalse(is_user.exists())

    @tag("user-signup")
    def test_user_signup_with_missing_fields(self):
        """Test given an incomplete or wrong body field data, no user is created"""

        del self.data["email"]

        response = self.client.post("/auth/signup", self.data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json_data["error_code"], 1304)
        self.assertNotEquals(json_data["data"], {})
        self.assertFalse(json_data["success"])

        is_user = UserFactory.filter(
            first_name=self.data["first_name"], last_name=self.data["last_name"]
        )

        self.assertFalse(is_user.exists())

    @tag("admin-signup")
    def test_admin_user_signup(self):
        """Test given valid sign up data, admin user is created"""

        response = self.client.post("/auth/admin/signup", self.data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(json_data["success"])

        with self.assertRaises(KeyError):
            json_data["error_code"]

        is_user = UserFactory.filter(email=self.data["email"])

        self.assertTrue(is_user.exists())

        user = is_user.get()

        self.assertTrue(user.is_staff)
        self.assertEquals(user.user_type, UserTypes["AdminUser"].value)

    @tag("admin-signup")
    def test_admin_user_signup_with_existing_email(self):
        """Test given an invalid data such as an already existing email, no admin user is created"""

        UserFactory(is_staff=True, user_type=UserTypes["AdminUser"].value)

        self.data["first_name"], self.data["last_name"] = "cool", "kid"

        response = self.client.post("/auth/admin/signup", self.data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(json_data["success"])
        self.assertEquals(json_data["error_code"], 1304)

        is_user = UserFactory.filter(
            first_name=self.data["first_name"], last_name=self.data["last_name"]
        )

        self.assertFalse(is_user.exists())

    @tag("login")
    def test_login_with_valid_credentials(self):
        """Test given a valid user credentials, access token is returned in response object"""

        UserFactory()

        data = dict()
        data["email"], data["password"] = self.data["email"], self.data["password"]

        response = self.client.post("/auth/login", data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", json_data["data"])
        self.assertNotIn("error_code", json_data)
        self.assertTrue(json_data["success"])
        self.assertIsInstance(json_data["data"]["access_token"], str)
        self.assertTrue(len(json_data["data"]["access_token"]) > 5)

    @tag("login")
    def test_login_with_invalid_credentials(self):
        """Test given invalid login credentials, error is thrown and access token isn't passed"""

        UserFactory()

        data = dict()
        data["password"] = "password"
        data["email"] = self.data["email"]

        response = self.client.post("/auth/login", data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error_code", json_data)
        self.assertFalse(json_data["success"])
        self.assertNotIn("access_token", json_data["data"])
        self.assertEquals(json_data["error_code"], 1301)

    @tag("login")
    def test_login_with_missing_fields(self):
        """Test given an incomplete or wrong body field data, no access token is passed"""

        del self.data["email"]

        response = self.client.post("/auth/login", self.data)

        json_data = response.json()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error_code", json_data)
        self.assertFalse(json_data["success"])
        self.assertNotIn("access_token", json_data["data"])
        self.assertEquals(json_data["error_code"], 1304)

    @tag("logout")
    def test_logout(self):
        """Test user token is deleted on logout"""

        UserFactory()

        login_endpoint = "/auth/login"
        logout_endpoint = "/auth/logout"

        data = dict()
        data["email"], data["password"] = self.data["email"], self.data["password"]

        access_token = self.client.post(login_endpoint, data).json()["data"]["access_token"]

        request_headers = {
            "content-type": "Application/json",
            "HTTP_AUTHORIZATION": f"Bearer {access_token}",
        }

        response = self.client.get(logout_endpoint, data, **request_headers)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        second_response_call_to_protected_route = self.client.post(
            logout_endpoint, data, **request_headers
        )

        self.assertEquals(
            second_response_call_to_protected_route.status_code, status.HTTP_401_UNAUTHORIZED
        )
