from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def get_fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def create_user(self, email, password, kwargs):

        if email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("first_name", kwargs.get("first_name", None))
        kwargs.setdefault("last_name", kwargs.get("last_name", None))

        return self.create_user(email, password, kwargs)
