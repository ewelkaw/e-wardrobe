from django.views.generic import View
from ewardrobe_app.models import Product, Basket, ProductsAmount
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from ewardrobe_app.queries.order import OrderQuery


class OrderView(View):
    template_name = "order.html"
    failure_url = "products"

    def post(self, request):
        product_id = request.POST.get("product_id")
        amount = request.POST.get("amount")
        size = request.POST.get("size")

        if request.user.is_authenticated:
            response = OrderQuery(
                product_id, request.user, amount, size
            ).add_product_to_basket()
            return render(
                request,
                self.template_name,
                {
                    "basket": response[0],
                    "products_amounts": response[1],
                    "product": response[2],
                    "total_cost": response[3],
                },
            )
        else:
            return redirect(reverse(self.failure_url), id=product_id)
