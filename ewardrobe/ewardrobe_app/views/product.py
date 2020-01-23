from django.views.generic import View
from ewardrobe_app.models import Product
from django.shortcuts import render, redirect
from django.urls import reverse


class ProductView(View):
    template_name = "product.html"
    failure_url = "main"

    def get(self, request):
        if request.user.is_authenticated:
            id = request.GET.get("id")
            product = Product.objects.filter(id=id)
            return render(request, self.template_name, {"product": product})
        else:
            return redirect(reverse(self.failure_url))
