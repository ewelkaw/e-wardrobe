from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .factories import ProductFactory


class ProductsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(
            username="john", email="lennon@thebeatles.com", password="johnpassword"
        )
        ProductFactory.create_batch(40)

    def test_basket_logged_out_view(self):
        result = self.client.post(
            "/basket/", {"product_id": 1, "amount": "2", "size": "S"}
        )
        assert result.status_code == 302

    def test_basket_logged_in_view(self):
        self.client.post(
            "/login/", {"username": "john", "password": "johnpassword"},
        )
        result = self.client.post(
            "/basket/", {"product_id": 1, "amount": "2", "size": "S"}
        )
        assert result.status_code == 200
