from django.contrib import admin
from django.utils.html import format_html

from django.urls import reverse

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
    date_heirarchy = ("date_created",)
    list_display = (
        "id",
        "user",
        "status",
        "date_modified",
        "date_created",
    )
    readonly_fields = (
        "id",
        "user",
        "date_modified",
        "date_created",
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "product_category", "retailer")


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductsAmount)
