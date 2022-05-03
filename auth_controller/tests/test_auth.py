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

    def test_user_signup_with_missing_fields(self):
        """Test given in complete or wrong body field data, no user is created"""

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

    def _test_login_with_valid_credentialsl(self):
        pass

    def _test_login_with_invalid_credentials(self):
        pass

    def _test_logout(self):
        pass
