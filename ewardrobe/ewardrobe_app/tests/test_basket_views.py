from django.test import TestCase
from django.test import Client
from .factories import ProductFactory, UserFactory


class BasketViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.product = ProductFactory()

    def test_basket_logged_out_view(self):
        result = Client().post(
            "/basket/", {"product_id": 1, "amount": "2", "size": "S"}
        )
        assert result.status_code == 302

    def test_basket_logged_in_view(self):
        client = Client()
        client.force_login(self.user)
        result = client.post(
            "/basket/", {"product_id": self.product.id, "amount": "2", "size": "S"}
        )
        assert result.status_code == 200
