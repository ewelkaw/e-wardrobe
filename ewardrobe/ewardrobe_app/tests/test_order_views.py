from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from ewardrobe_app.models import (
    Product,
    Brand,
    Category,
    Retailer,
    Color,
)


class OrderViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(
            username="john", email="lennon@thebeatles.com", password="johnpassword"
        )
        cls.brand = Brand.objects.create(name="brand")
        cls.category = Category.objects.create(name="category")
        cls.retailer = Retailer.objects.create(name="retailer")
        cls.color = Color.objects.create(name="color")
        cls.product = Product.objects.create(
            name="t-shirt",
            price=20.00,
            url="https://my_shirt.com",
            description="t-shirt description",
            rating=4.5,
            review_count=13,
            brand=cls.brand,
            product_category=cls.category,
            retailer=cls.retailer,
            color=cls.color,
        )

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
            "/basket/", {"product_id": self.product.id, "amount": "2", "size": "S"}
        )
        assert result.status_code == 200
