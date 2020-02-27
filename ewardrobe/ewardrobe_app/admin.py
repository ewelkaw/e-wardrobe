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

    # def process_deposit(self, request, *args, **kwargs):
    #     return self.process_action(request=request, action_title="Ship")

    # def process_withdraw(self, request, *args, **kwargs):
    #     return self.process_action(request=request, action_title="Close")

    # def basket_actions(self, obj):
    #     if obj.status == STATUS_PAID:
    #         return format_html(
    #             '<a class="button" href="{}">Ship</a>&nbsp;',
    #             reverse("admin:admin", kwargs={"ship": "ship", "basket": obj.id}),
    #         )
    #     if obj.status == STATUS_SHIPPED:
    #         return format_html(
    #             '<a class="button" href="{}">Close</a>&nbsp;',
    #             reverse("admin:admin", kwargs={"close": "close", "basket": obj.id}),
    #         )

    # basket_actions.short_description = "Basket Actions"
    # basket_actions.allow_tags = True

    # def process_action(self, request, action_title):
    #     account = self.get_object(request, account_id)
    #     if request.method != 'POST':


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "product_category", "retailer")


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductsAmount)
