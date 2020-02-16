from django.test import TestCase
from django.test import Client
from .factories import ProductFactory, UserFactory


class ProductViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.product = ProductFactory()

    def test_product_regular_logged_out_view(self):
        result = Client().get("/products/", kwargs={"id": self.product.id})
        assert result.status_code == 302

    def test_product_regular_view(self):
        client = Client()
        client.force_login(self.user)
        result = client.get("/products/", kwargs={"id": self.product.id})

        assert result.status_code == 200
