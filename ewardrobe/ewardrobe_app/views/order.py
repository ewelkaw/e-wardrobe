from django.views.generic import View
from ewardrobe_app.models import Product, Basket, ProductsAmount
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse


class OrderView(View):
    template_name = "order.html"
    failure_url = "product"

    def post(self, request):

        if request.user.is_authenticated:
            product_id = request.POST.get("product_id")
            amount = request.POST.get("amount")
            size = request.POST.get("size")

            product = Product.objects.get(id=product_id)
            basket, _ = Basket.objects.get_or_create(status=0, user=request.user)
            basket.save()

            product_amount, _ = ProductsAmount.objects.get_or_create(
                basket=basket, product=product, size=size
            )
            product_amount.amount += int(amount)
            product_amount.save()

            products_amounts = ProductsAmount.objects.filter(basket=basket).all()

            return render(
                request,
                self.template_name,
                {
                    "basket": basket,
                    "products_amounts": products_amounts,
                    "product": product,
                    "total_cost": sum(
                        products_amount.cost for products_amount in products_amounts
                    ),
                },
            )
        else:
            return redirect(reverse(self.failure_url), id=product_id)
