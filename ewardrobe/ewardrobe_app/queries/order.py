from ewardrobe_app.models import Product, Basket, ProductsAmount
from django.contrib.auth.models import User


class OrderWorkflow:
    def __init__(
        self, product_id: int, user: User, amount: int, size: str,
    ):
        self.__product_id = product_id
        self.__user = user
        self.__amount = amount
        self.__size = size

    def add_product_to_basket(self) -> dict:
        product = Product.objects.get(id=self.__product_id)
        basket, _ = Basket.objects.get_or_create(status=0, user=self.__user)

        product_amount, _ = ProductsAmount.objects.get_or_create(
            basket=basket, product=product, size=self.__size
        )
        product_amount.amount += int(self.__amount)
        product_amount.save()

        products_amounts = ProductsAmount.objects.filter(basket=basket).all()

        # in case of performace it can be an issue,
        # but we assume there will be a reasonable amount of products in a single basket
        total_cost = sum(products_amount.cost for products_amount in products_amounts)
        return {
            "basket": basket,
            "products_amounts": products_amounts,
            "product": product,
            "total_cost": total_cost,
        }

