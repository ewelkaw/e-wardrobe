from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.views.main import ChangeList
from ewardrobe_app.models import STATUS_PAID, STATUS_SHIPPED

from django.urls import reverse, re_path

from .models import (
    Brand,
    Category,
    Retailer,
    Product,
    Basket,
    ProductsAmount,
    STATUS_PAID,
    STATUS_SHIPPED,
)

# Register your models here.


class BasketAdmin(admin.ModelAdmin):
    # date_hierarchy = ("date_created",)
    list_display = (
        "id",
        "user",
        "status",
        "date_modified",
        "date_created",
        "basket_actions",
    )
    readonly_fields = (
        "id",
        "user",
        "status",
        "date_modified",
        "date_created",
    )

    def process_shipment(self):
        pass

    def process_closing(self):
        pass

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^(?P<basket_id>.+)/ship/$",
                self.admin_site.admin_view(self.process_shipment),
                name="basket-ship",
            ),
            re_path(
                r"^(?P<basket_id>.+)/close/$",
                self.admin_site.admin_view(self.process_closing),
                name="basket-close",
            ),
        ]
        return custom_urls + urls

    def basket_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Ship</a>&nbsp;'
            '<a class="button" href="{}">Close</a>',
            reverse("admin:basket-ship", args=[obj.pk]),
            reverse("admin:basket-close", args=[obj.pk]),
        )

    basket_actions.short_description = "Basket Actions"
    basket_actions.allow_tags = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "product_category", "retailer")


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductsAmount)
