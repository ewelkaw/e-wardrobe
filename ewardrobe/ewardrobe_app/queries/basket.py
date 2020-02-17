from ewardrobe_app.models import Product, Basket, ProductsAmount
from django.contrib.auth.models import User


class BasketWorkflow:
    def __init__(
        self,
        user: User,
        product_id: int = None,
        size: str = None,
        amount: int = 0,
        action=None,
    ):
        self.__product_id = product_id
        self.__user = user
        self.__amount = amount
        self.__size = size
        self.__action = action

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
        return {
            "basket": basket,
            "products_amounts": products_amounts,
            "product": product,
            "total_cost": self.__calculate_total_cost(products_amounts),
        }

    def get_current_basket(self) -> dict:
        basket, _ = Basket.objects.get_or_create(status=0, user=self.__user)
        products_amounts = ProductsAmount.objects.filter(basket=basket).all()

        return {
            "basket": basket,
            "products_amounts": products_amounts,
            "product": None,
            "total_cost": self.__calculate_total_cost(products_amounts),
        }

    def change_product_amount(self) -> dict:
        product = Product.objects.get(id=self.__product_id)
        basket = Basket.objects.get(status=0, user=self.__user)
        product_amount = ProductsAmount.objects.get(
            basket=basket, product=product, size=self.__size
        )
        # import ipdb

        # ipdb.set_trace()
        if self.__action == "+":
            product_amount.amount += 1
        elif self.__action == "-":
            product_amount.amount -= 1
        product_amount.save()

        products_amounts = ProductsAmount.objects.filter(basket=basket).all()
        return {
            "basket": basket,
            "products_amounts": products_amounts,
            "product": None,
            "total_cost": self.__calculate_total_cost(products_amounts),
        }

    def delete_from_basket(self) -> dict:
        product = Product.objects.get(id=self.__product_id)
        basket = Basket.objects.get(status=0, user=self.__user)
        product_amount = ProductsAmount.objects.get(
            basket=basket, product=product, size=self.__size
        ).delete()

        products_amounts = ProductsAmount.objects.filter(basket=basket).all()

        # in case of performace it can be an issue,
        # but we assume there will be a reasonable amount of products in a single basket
        return {
            "basket": basket,
            "products_amounts": products_amounts,
            "product": None,
            "total_cost": self.__calculate_total_cost(products_amounts),
        }

    def __calculate_total_cost(self, products_amounts):
        return sum(products_amount.cost for products_amount in products_amounts)
