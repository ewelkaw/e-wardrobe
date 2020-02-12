from ewardrobe_app.models import Product
from django.core.paginator import Paginator, Page


class ProductsQuery:
    def __init__(self, page_number: int, paginate_by: int = 20, q: str = None):
        self.__page_number = page_number
        self.__paginate_by = paginate_by
        self.__q = q

    def get_products_and_links(self) -> tuple:
        if not self.__q:
            products = Product.objects.all()
            paginator = Paginator(products, self.__paginate_by)
        else:
            products = Product.objects.filter(name__icontains=self.__q)
            paginator = Paginator(products, self.__paginate_by)
        page_object = paginator.get_page(self.__page_number)
        return page_object, self.__prepare_links(page_object)

    def __prepare_links(self, page_obj: Page) -> dict:
        output = dict()
        if page_obj.has_previous():
            output["previous"] = f"?page={page_obj.previous_page_number()}"
        if page_obj.has_next():
            output["next"] = f"?page={page_obj.next_page_number()}"
        if self.__q:
            for key in output.keys():
                output[key] += f"&q={self.__q}"
        return output
