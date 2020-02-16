from django.test import TestCase
from ewardrobe_app.queries.order import OrderWorkflow
from .factories import ProductFactory, UserFactory
from ewardrobe_app.models import Basket, ProductsAmount


class OrderWorkflowTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.product1 = ProductFactory()
        cls.product2 = ProductFactory()

    def test_order_zero_products_in_basket(self):
        result = OrderWorkflow(
            product_id=self.product1.id, user=self.user, amount=0, size="S"
        ).add_product_to_basket()
        basket = Basket.objects.first()
        assert result["basket"] == basket
        self.assertQuerysetEqual(
            result["products_amounts"],
            ProductsAmount.objects.filter(basket=basket).all(),
            transform=lambda x: x,
        )
        assert result["product"] == self.product1
        assert result["total_cost"] == 0.00

    def test_order_single_product_in_basket(self):
        result = OrderWorkflow(
            product_id=self.product1.id, user=self.user, amount=1, size="S"
        ).add_product_to_basket()
        basket = Basket.objects.first()
        assert result["basket"] == basket
        self.assertQuerysetEqual(
            result["products_amounts"],
            ProductsAmount.objects.filter(basket=basket).all(),
            transform=lambda x: x,
        )
        assert result["product"] == self.product1
        assert result["total_cost"] == self.product1.price

    def test_order_multiple_products_in_basket(self):
        # adding first products
        result1 = OrderWorkflow(
            product_id=self.product1.id, user=self.user, amount=2, size="S"
        ).add_product_to_basket()
        basket = Basket.objects.first()

        assert result1["basket"] == basket
        self.assertQuerysetEqual(
            result1["products_amounts"],
            ProductsAmount.objects.filter(basket=basket).all(),
            transform=lambda x: x,
        )
        assert result1["product"] == self.product1
        assert result1["total_cost"] == 2 * self.product1.price

        # adding next products
        result2 = OrderWorkflow(
            product_id=self.product2.id, user=self.user, amount=3, size="M"
        ).add_product_to_basket()
        basket = Basket.objects.first()
        assert result2["basket"] == basket
        self.assertQuerysetEqual(
            result2["products_amounts"],
            ProductsAmount.objects.filter(basket=basket).all(),
            transform=lambda x: x,
            ordered=False,
        )
        assert result2["product"] == self.product2
        assert (
            result2["total_cost"] == 2 * self.product1.price + 3 * self.product2.price
        )
