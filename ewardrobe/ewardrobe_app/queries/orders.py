from ewardrobe_app.models import Basket
from django.contrib.auth.models import User
from ewardrobe_app.models import STATUS_CHOICES


TRANSITIONS = {
    0: ["Pay", "Cancel"],
    1: ["Shiping"],
    2: ["Close", "Return"],
}


class OrderWorkflow:
    def __init__(self, user: User):
        self.__user = user

    def prepare_baskets(self) -> dict:
        orders = Basket.objects.filter(user=self.__user).order_by("-date_created").all()
        orders_data = []
        for idx, order in enumerate(orders):
            orders_data.append(
                {
                    "order": order,
                    "status_name": STATUS_CHOICES[order.status][1].capitalize(),
                    "avaliable_statuses": TRANSITIONS.get(order.status, []),
                }
            )

        return {
            "orders_data": orders_data,
        }
