from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from django_fsm import TransitionNotAllowed
from ewardrobe_app.models import (
    Product,
    Basket,
    ProductsAmount,
    Brand,
    Category,
    Retailer,
    Color,
)


class BasketTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="john", email="lennon@thebeatles.com", password="johnpassword"
        )
        cls.user1 = User.objects.create_user(
            username="john2", email="lennon@thebeatles.com", password="johnpassword"
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

    def test_new_basket(self):
        basket = Basket.objects.create(user=self.user)
        basket.add_product(self.product)

        assert ProductsAmount.objects.count() == 1
        assert ProductsAmount.objects.first().product == self.product
        assert ProductsAmount.objects.first().amount == 1
        assert ProductsAmount.objects.first().cost == 20.00

        basket.add_product(self.product)

        assert ProductsAmount.objects.count() == 1
        assert ProductsAmount.objects.first().amount == 2
        assert ProductsAmount.objects.first().cost == 40.00

    def test_basket_open_close_flow(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        basket.pay()
        assert basket.status == 1

        basket.ship()
        assert basket.status == 2

        basket.close()
        assert basket.status == 3

    def test_basket_open_return_flow(self):
        basket = Basket.objects.create(user=self.user)

        assert basket.status == 0

        basket.pay()
        assert basket.status == 1

        basket.ship()
        assert basket.status == 2

        basket.give_back()
        assert basket.status == 5

    def test_basket_open_cancel_flow(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        basket.cancel()
        assert basket.status == 4

    def test_basket_give_back_status_fail(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        with pytest.raises(TransitionNotAllowed):
            basket.give_back()

    def test_basket_shipped_status_fail(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        with pytest.raises(TransitionNotAllowed):
            basket.ship()

    def test_basket_closed_status_fail(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        with pytest.raises(TransitionNotAllowed):
            basket.close()

    def test_basket_paid_status_fail(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0
        basket.cancel()

        with pytest.raises(TransitionNotAllowed):
            basket.pay()
