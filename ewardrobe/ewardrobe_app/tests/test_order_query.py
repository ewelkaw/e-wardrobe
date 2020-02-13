from django.test import TestCase
from ewardrobe_app.queries.order import OrderWorkflow
from django.contrib.auth.models import User
from ewardrobe_app.models import (
    Product,
    Basket,
    ProductsAmount,
    Brand,
    Category,
    Retailer,
    Color,
)


class OrderWorkflowTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="john", email="lennon@thebeatles.com", password="johnpassword"
        )
        cls.brand = Brand.objects.create(name="brand")
        cls.category = Category.objects.create(name="category")
        cls.retailer = Retailer.objects.create(name="retailer")
        cls.color = Color.objects.create(name="color")
        cls.product1 = Product.objects.create(
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
        cls.product2 = Product.objects.create(
            name="socks",
            price=50.00,
            url="https://socks.com",
            description="socks description",
            rating=3.5,
            review_count=42,
            brand=cls.brand,
            product_category=cls.category,
            retailer=cls.retailer,
            color=cls.color,
        )

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
        assert result["total_cost"] == 20.00

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
        assert result1["total_cost"] == 40.00

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
        assert result2["total_cost"] == 190.00
