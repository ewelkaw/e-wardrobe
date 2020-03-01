from django.test import TestCase
import pytest
from ewardrobe_app.tests.factories import ProductFactory, UserFactory
from django_fsm import TransitionNotAllowed
from ewardrobe_app.models import Basket, ProductsAmount


class BasketTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.product = ProductFactory()

    def test_new_basket(self):
        basket = Basket.objects.create(user=self.user)
        basket.add_product(self.product)

        assert ProductsAmount.objects.count() == 1
        assert ProductsAmount.objects.first().product == self.product
        assert ProductsAmount.objects.first().amount == 1
        assert ProductsAmount.objects.first().cost == self.product.price

        basket.add_product(self.product)

        assert ProductsAmount.objects.count() == 1
        assert ProductsAmount.objects.first().amount == 2
        assert ProductsAmount.objects.first().cost == 2 * self.product.price

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
        assert basket.status == 4

    def test_basket_open_pay_flow(self):
        basket = Basket.objects.create(user=self.user)
        assert basket.status == 0

        basket.pay()
        assert basket.status == 1

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
        basket.pay()
        basket.ship()

        with pytest.raises(TransitionNotAllowed):
            basket.pay()
