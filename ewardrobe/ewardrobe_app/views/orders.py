from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from ewardrobe_app.models import Basket, ProductsAmount
from ewardrobe_app.queries.orders import OrderWorkflow


class OrdersView(View):
    template_name = "orders.html"
    failure_url = "login"

    def post(self, request):
        if request.user.is_authenticated:
            basket_id = request.POST.get("basket")
            basket = Basket.objects.get(user=request.user, id=basket_id)

            if request.POST.get("pay"):
                if ProductsAmount.objects.filter(basket=basket).all():
                    basket.pay()

            if request.POST.get("cancel"):
                basket.cancel()

            if request.POST.get("ship"):
                basket.ship()

            if request.POST.get("give_back"):
                basket.give_back()

            if request.POST.get("close"):
                basket.close()

            basket.save()
            return render(
                request,
                self.template_name,
                {"orders_data": OrderWorkflow(request.user).prepare_baskets()},
            )
        else:
            return redirect(reverse(self.failure_url))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                self.template_name,
                {"orders_data": OrderWorkflow(request.user).prepare_baskets()},
            )
        else:
            return redirect(reverse(self.failure_url))

