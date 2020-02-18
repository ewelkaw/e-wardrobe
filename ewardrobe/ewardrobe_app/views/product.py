from django.views.generic import View
from ewardrobe_app.models import Product
from django.shortcuts import render, redirect
from django.urls import reverse


class ProductView(View):
    template_name = "product.html"
    failure_url = "login"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=kwargs["id"])
            return render(request, self.template_name, {"product": product})
        else:
            return redirect(reverse(self.failure_url))
