from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from datetime import datetime
from django.shortcuts import redirect, reverse

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
    ordering = ["date_modified"]
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
        "basket_actions",
    )

    def process_shipment(self, request, *args, **kwargs):
        basket_id = kwargs["basket_id"]
        basket = Basket.objects.get(id=basket_id)
        basket.ship()
        basket.save()
        return redirect(reverse("admin:ewardrobe_app_basket_changelist"))

    def process_closing(self, request, *args, **kwargs):
        basket_id = kwargs["basket_id"]
        basket = Basket.objects.get(id=basket_id)
        basket.close()
        basket.save()
        return redirect(reverse("admin:ewardrobe_app_basket_changelist"))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:basket_id>/ship",
                self.admin_site.admin_view(self.process_shipment),
                name="basket-ship",
            ),
            path(
                "<int:basket_id>/close",
                self.admin_site.admin_view(self.process_closing),
                name="basket-close",
            ),
        ]
        return custom_urls + urls

    def basket_actions(self, basket):
        if basket.status == STATUS_PAID:
            return format_html(
                '<a class="button" href="{}">Ship</a>&nbsp;',
                reverse("admin:basket-ship", args=[basket.id]),
            )

        if basket.status == STATUS_SHIPPED and self.count_closing_date(
            basket.date_modified
        ):
            return format_html(
                '<a class="button" href="{}">Close</a>',
                reverse("admin:basket-close", args=[basket.id]),
            )

    @staticmethod
    def count_closing_date(date_modified):
        return (datetime.now().date() - date_modified).days > 14

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
