from django.test import TestCase
from ewardrobe_app.workflows.orders import OrderWorkflow
from .factories import ProductFactory, UserFactory
from ewardrobe_app.models import (
    Basket,
    ProductsAmount,
    STATUS_OPENED,
    STATUS_PAID,
    STATUS_SHIPPED,
    STATUS_CLOSED,
    STATUS_RETURNED,
)


class BasketWorkflowTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = ProductFactory()
        for status in [
            STATUS_OPENED,
            STATUS_PAID,
            STATUS_SHIPPED,
            STATUS_SHIPPED,
            STATUS_CLOSED,
            STATUS_RETURNED,
        ]:
            cls.user = UserFactory(username="user_{}".format())
            cls.basket = Basket.object.create(user=cls.user, status=status)
            cls.products_amount = ProductsAmount(
                basket=cls.basket, product=cls.product, size="S"
            )

    def test_orders_workflow(self):
        orders = OrderWorkflow(self.user).prepare_baskets()

        assert len(orders) == 5
