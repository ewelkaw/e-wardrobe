from ewardrobe_app.models import Basket
from django.contrib.auth.models import User
from ewardrobe_app.models import STATUS_CHOICES, STATUS_OPENED


class OrderWorkflow:
    def __init__(self, user: User):
        self.__user = user

    def prepare_baskets(self) -> dict:
        orders_data = []
        for idx, order in enumerate(
            Basket.objects.filter(user=self.__user)
            .exclude(status=STATUS_OPENED)
            .order_by("-date_created")
        ):

            orders_data.append(
                {
                    "order": order,
                    "status_name": STATUS_CHOICES[order.status][1].capitalize(),
                    "avaliable_statuses": self.__prepare_transitions(order),
                }
            )

        return orders_data

    def __prepare_transitions(self, order: Basket) -> list:
        return [
            transition.name.capitalize()
            for transition in list(order.get_available_status_transitions())
        ]

