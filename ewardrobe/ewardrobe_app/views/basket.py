from django.views.generic import View
from ewardrobe_app.models import Product, Basket, 
from django.shortcuts import render, redirect
from django.urls import reverse

class BasketView(View):
    template_name = "order.html"
    failure_url = "product"

    def post(self, request):
        if request.user.is_authenticated:
            product_id = request.POST.get("product_id")
            amount = request.POST.get("amount")
            size = request.POST.get("size")

            product = Product.objects.get(id=product_id)
            basket = Basket.objects.get_or_create(status=0, user=request.user.id)
            product_amount = ProductsAmount(basket=basket, product=product, size=size, amount=amount)
            return render(request, self.template_name, {"basket": basket})
        else:
            return redirect(reverse(self.failure_url), id=product_id))

