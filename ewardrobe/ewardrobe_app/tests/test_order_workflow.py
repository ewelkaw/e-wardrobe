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
        cls.product = ProductFactory()
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        for idx, status in enumerate(
            [
                STATUS_OPENED,
                STATUS_PAID,
                STATUS_SHIPPED,
                STATUS_SHIPPED,
                STATUS_CLOSED,
                STATUS_RETURNED,
            ]
        ):
            if status == STATUS_SHIPPED and idx == 2:
                date = datetime.date.today() - datetime.timedelta(days=15)
                cls.basket = Basket.objects.create(
                    user=cls.user2, status=status, date_modified=date,
                )
                print("1", cls.basket.date_modified)
            if status == STATUS_SHIPPED and idx == 3:
                cls.basket = Basket.objects.create(user=cls.user2, status=status)
                print("2", cls.basket.date_modified)
            else:
                cls.basket = Basket.objects.create(user=cls.user1, status=status)
                print("3", cls.basket.date_modified)
            cls.products_amount = ProductsAmount(
                basket=cls.basket, product=cls.product, size="S"
            )
            # orders[0]['order'].date_modified

        orders = OrderWorkflow(user=cls.user2).prepare_baskets()
        import ipdb

        ipdb.set_trace()

    def test_orders_non_return_status_workflow(self):
        orders = OrderWorkflow(user=self.user1).prepare_baskets()
        for order in orders:
            assert isinstance(order["order"], Basket)
            assert order["status_name"] in ["Paid", "Closed", "Returned"]
            assert not order["return_status"]
        assert len(orders) == 3

    def test_orders_return_status_workflow(self):
        orders = OrderWorkflow(user=self.user2).prepare_baskets()
        for order in orders:
            assert isinstance(order["order"], Basket)
            assert order["status_name"] in ["Shipped"]
            # assert order["return_status"]
            assert (
                order["return_status"]
                if order["order"].date_modified == datetime.date.today()
                else not order["return_status"]
            )
        assert len(orders) == 2

