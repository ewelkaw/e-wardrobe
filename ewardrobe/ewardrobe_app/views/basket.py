from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from ewardrobe_app.queries.basket import BasketWorkflow


class BasketView(View):
    template_name = "basket.html"
    failure_url = "products"

    def post(self, request):
        change = request.POST.get("change")
        delete = request.POST.get("delete")
        product_id = request.POST.get("product_id")
        amount = request.POST.get("amount")
        size = request.POST.get("size")

        if request.user.is_authenticated:
            if change:
                response = BasketWorkflow(
                    request.user, product_id, size, 0, change
                ).change_product_amount()
            elif delete:
                response = BasketWorkflow(
                    request.user, product_id, size
                ).delete_from_basket()
            else:
                response = BasketWorkflow(
                    request.user, product_id, size, amount
                ).add_product_to_basket()
            return render(request, self.template_name, response)
        else:
            return redirect(reverse(self.failure_url), id=product_id)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            response = BasketWorkflow(request.user).get_current_basket()
            return render(request, self.template_name, response)
        else:
            return redirect(reverse(self.failure_url))
