from datetime import datetime

from ewardrobe_app.models import Basket
from django.contrib.auth.models import User
from ewardrobe_app.models import STATUS_CHOICES, STATUS_OPENED, STATUS_RETURNED


class OrderWorkflow:
    def __init__(self, user: User):
        self.__user = user

    def prepare_baskets(self) -> dict:
        orders_data = []
        for order in (
            Basket.objects.filter(user=self.__user)
            .exclude(status=STATUS_OPENED)
            .order_by("-date_modified")
        ):
            orders_data.append(
                {
                    "order": order,
                    "status_name": STATUS_CHOICES[order.status][1].capitalize(),
                    "return_status": self.check_return_transition(order)
                    and self.count_returning_date(order.date_modified),
                }
            )

        return orders_data

    @staticmethod
    def check_return_transition(order: Basket) -> bool:
        transitions = list(order.get_available_status_transitions())
        return STATUS_RETURNED in [transition.target for transition in transitions]

    @staticmethod
    def count_returning_date(date_modified):
        return (datetime.now().date() - date_modified).days <= 14
