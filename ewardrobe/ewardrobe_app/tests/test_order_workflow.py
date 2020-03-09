import datetime

from django.test import TestCase
from ewardrobe_app.workflows.orders import OrderWorkflow
from .factories import ProductFactory, UserFactory
from django.contrib.auth.models import User
from ewardrobe_app.models import (
    Basket,
    ProductsAmount,
    STATUS_OPENED,
    STATUS_PAID,
    STATUS_SHIPPED,
    STATUS_CLOSED,
    STATUS_RETURNED,
)


class OrderWorkflowTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        date = datetime.date.today() - datetime.timedelta(days=15)
        cls.product = ProductFactory()
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        for status in [
            STATUS_OPENED,
            STATUS_PAID,
            STATUS_SHIPPED,
            STATUS_CLOSED,
            STATUS_RETURNED,
        ]:
            cls.basket = Basket.objects.create(user=cls.user1, status=status)
            Basket.objects.filter(id=cls.basket.id).update(date_modified=date)
            cls.products_amount = ProductsAmount(
                basket=cls.basket, product=cls.product, size="S"
            )

        # setup one shipped basket with 14 days return period
        cls.basket = Basket.objects.create(user=cls.user2, status=STATUS_SHIPPED)

    def test_orders_non_return_status_workflow(self):
        orders = OrderWorkflow(user=self.user1).prepare_baskets()
        for order in orders:
            assert isinstance(order["order"], Basket)
            assert order["status_name"] in ["Paid", "Closed", "Returned", "Shipped"]
            assert not order["return_status"]
        assert len(orders) == 4

    def test_orders_return_status_workflow(self):
        orders = OrderWorkflow(user=self.user2).prepare_baskets()
        assert isinstance(orders[0]["order"], Basket)
        assert orders[0]["status_name"] in ["Shipped"]
        assert orders[0]["return_status"]
        assert len(orders) == 1

