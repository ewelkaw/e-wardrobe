from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from ewardrobe_app.models import Basket
from ewardrobe_app.queries.orders import OrderWorkflow


class OrdersView(View):
    template_name = "orders.html"
    failure_url = "login"

    def post(self, request):
        if request.user.is_authenticated:
            basket_id = request.POST.get("basket")
            basket = Basket.objects.filter(user=request.user, id=basket_id)
            action = request.POST.get("action", None)

            # print("basket_id", basket_id, "basket", basket, "action", action)
            if action == "Pay":
                basket.pay()

            if action == "Cancel":
                basket.cancel()

            if action == "Ship":
                basket.ship()

            if action == "Give back":
                basket.give_back()

            if action == "Close":
                basket.close()

            return render(
                request,
                self.template_name,
                OrderWorkflow(request.user).prepare_baskets(),
            )
        else:
            return redirect(reverse(self.failure_url))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(
                request,
                self.template_name,
                OrderWorkflow(request.user).prepare_baskets(),
            )
        else:
            return redirect(reverse(self.failure_url))

