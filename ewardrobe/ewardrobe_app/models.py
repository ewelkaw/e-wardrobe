from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class DateAddedMixin(models.Model):
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Brand(models.Model):
    brand_name = models.CharField(max_length=25)


class Category(models.Model):
    category = models.CharField(max_length=25)


class Retailer(models.Model):
    retailer = models.CharField(max_length=25)


class Color(models.Model):
    color = models.CharField(max_length=25)


class Product(DateAddedMixin, models.Model):
    class Size(Enum):
        XS = ("XS", "XS")
        S = ("S", "S")
        M = ("M", "M")
        L = ("L", "L")
        XL = ("XL", "XL")
        XXL = ("XXL", "XXL")

        @classmethod
        def get_value(cls, member):
            return cls[member].value

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.URLField()
    description = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    reviews_count = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    size = models.CharField(
        max_length=4, choices=[x.value for x in Size], default=Size.get_value("M"),
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["date_added", "name"]


class Basket(DateAddedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    products = models.ManyToManyField(Product, through="ProductsAmount")

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user


class ProductsAmount(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.product
