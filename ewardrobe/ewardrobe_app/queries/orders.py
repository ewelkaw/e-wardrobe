from ewardrobe_app.models import Basket
from django.contrib.auth.models import User


class OrderWorkflow:
    def __init__(self, user: User):
        self.__user = user

    def prepare_baskets(self) -> dict:
        baskets = (
            Basket.objects.filter(user=self.__user).order_by("-date_created").all()
        )
        return {"baskets": baskets}
