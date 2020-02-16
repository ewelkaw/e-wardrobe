from django.test import TestCase
from django.test import Client
from .factories import ProductFactory, UserFactory


class ProductsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        ProductFactory.create_batch(40)

    def test_products_regular_logged_out_view(self):
        result = Client().get("/products/")
        assert result.status_code == 302

    def test_products_regular_view(self):
        client = Client()
        client.force_login(self.user)
        result = client.get("/products/")
        assert result.status_code == 200

    def test_products_search_logged_out_view(self):
        result = Client().get("/products/?q='test'")
        assert result.status_code == 302

    def test_products_search_view(self):
        client = Client()
        client.force_login(self.user)
        result = client.get("/products/?q='test'")
        assert result.status_code == 200

