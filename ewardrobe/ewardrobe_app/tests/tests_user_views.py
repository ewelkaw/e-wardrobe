from django.test import TestCase
import pytest
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.


class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_welcome_view(self):
        result = self.client.get("/")
        assert result.status_code == 200

    def test_main_get_view(self):
        result = self.client.get("/main/")
        assert result.status_code == 302

    def test_logout_get_view(self):
        result = self.client.get("/logout/")
        assert result.status_code == 302

    def test_login_get_view(self):
        result = self.client.get("/login/")
        assert result.status_code == 200

    def test_register_get_view(self):
        result = self.client.get("/register/")
        assert result.status_code == 200

    def test_register_post_view_success(self):
        result = self.client.post(
            "/register/",
            {
                "username": "john",
                "password1": "smith123password",
                "password2": "smith123password",
            },
        )
        assert result.status_code == 302
        assert result.url == "/main/"
        assert User.objects.filter(username="john").count() == 1

    def test_register_post_view_failure(self):
        result = self.client.post("/register/", {},)
        assert result.status_code == 200

    def test_login_post_view_success(self):
        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        result = self.client.post(
            "/login/", {"username": "john", "password": "johnpassword"},
        )
        assert result.status_code == 302
        assert result.url == "/main/"

    def test_login_post_view_failure(self):
        User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        result = self.client.post(
            "/login/", {"username": "johnny", "password": "johnpassword"},
        )
        assert result.status_code == 200

