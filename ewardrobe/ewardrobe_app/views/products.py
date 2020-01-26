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
        if request.GET.get("q"):
            return self.__search(request, *args, **kwargs)
        return self.__paginated_products(request, *args, **kwargs)

    def __paginated_products(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            products = Product.objects.all()
            paginator = Paginator(
                products, self.paginate_by
            )  # Show 20 products per page.
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)
            links = self.__construct_links(page_obj)
            return render(
                request, self.template_name, {"page_obj": page_obj, "links": links}
            )
        else:
            return redirect(reverse(self.failure_url))

    def __search(self, request, *args, **kwargs):
        q = request.GET.get("q")
        products = Product.objects.filter(name__icontains=q)
        paginator = Paginator(products, self.paginate_by)  # Show 20 products per page.
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        links = self.__construct_links(page_obj, q)
        return render(
            request, self.template_name, {"page_obj": page_obj, "links": links}
        )

    def __construct_links(self, page_obj, q=None):
        output = dict()
        if page_obj.has_previous():
            output["previous"] = f"?page={page_obj.previous_page_number()}"
        if page_obj.has_next():
            output["next"] = f"?page={page_obj.next_page_number()}"
        if q:
            for key in output.keys():
                output[key] += f"&q={q}"
        return output

