from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DateAddedMixin(models.Model):
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name_plural = "Brands"


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class Retailer(models.Model):
    retailer = models.CharField(max_length=100)

    def __str__(self):
        return self.retailer

    class Meta:
        verbose_name_plural = "Retailers"


class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name_plural = "Colors"


class Product(DateAddedMixin, models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.URLField()
    description = models.CharField(max_length=800)
    rating = models.DecimalField(max_digits=6, decimal_places=2)
    review_count = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "_" + self.brand

    class Meta:
        ordering = ["date_added", "name"]
        verbose_name_plural = "Products"


class Basket(DateAddedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    products = models.ManyToManyField(Product, through="ProductsAmount")

    def __str__(self):
        return self.user + self.products

    class Meta:
        ordering = ["user"]
        verbose_name_plural = "Baskets"


class ProductsAmount(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.product

    class Meta:
        verbose_name_plural = "Products Amounts"
