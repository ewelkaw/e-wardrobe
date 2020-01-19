from django.contrib import admin

from .models import Brand, Category, Retailer, Color, Product, Basket, ProductsAmount

# Register your models here.


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "product_category", "retailer")


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
admin.site.register(ProductsAmount)
