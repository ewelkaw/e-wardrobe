from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from ewardrobe_app.queries.order import OrderWorkflow


class OrderView(View):
    template_name = "order.html"
    failure_url = "products"

    def post(self, request):
        product_id = request.POST.get("product_id")
        amount = request.POST.get("amount")
        size = request.POST.get("size")

        if request.user.is_authenticated:
            response = OrderWorkflow(
                product_id, request.user, amount, size
            ).add_product_to_basket()
            return render(request, self.template_name, response)
        else:
            return redirect(reverse(self.failure_url), id=product_id)
