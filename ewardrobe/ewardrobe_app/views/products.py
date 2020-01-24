from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from ewardrobe_app.models import Product
from django.core.paginator import Paginator


class ProductsView(View):
    template_name = "products.html"
    failure_url = "main"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            products = Product.objects.all()
            paginator = Paginator(
                products, self.paginate_by
            )  # Show 20 products per page.
            page_number = request.GET.get("page") if request.GET.get("page") else 1
            page_obj = paginator.get_page(page_number)
            return render(request, self.template_name, {"page_obj": page_obj})
        else:
            return redirect(reverse(self.failure_url))
