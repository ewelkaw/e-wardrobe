from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from ewardrobe_app.models import Product
from django.core.paginator import Paginator

from ewardrobe_app.queries.products import ProductsQuery


class ProductsView(View):
    template_name = "products.html"
    failure_url = "main"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            page_number = request.GET.get("page", 1)
            if request.GET.get("q"):
                return self.__show_searched_products(
                    request, page_number, *args, **kwargs
                )
            return self.__show_products(request, page_number, *args, **kwargs)
        else:
            return redirect(reverse(self.failure_url))

    def __show_products(self, request, page_number, *args, **kwargs):
        page_object, links = ProductsQuery(
            page_number, self.paginate_by
        ).get_products_and_links()
        return render(
            request, self.template_name, {"page_obj": page_object, "links": links}
        )

    def __show_searched_products(self, request, page_number, *args, **kwargs):
        q = request.GET.get("q")
        page_object, links = ProductsQuery(
            page_number, self.paginate_by, q
        ).get_products_and_links()
        return render(
            request, self.template_name, {"page_obj": page_object, "links": links}
        )
