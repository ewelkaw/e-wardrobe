from django.db import models
from enum import Enum

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField()


class Category(models.Model):
    category = models.CharField()


class Retailer(models.Model):
    retailer = models.CharField()


class Color(models.Model):
    color = models.CharField()


class Product(models.Model):
    class Size(Enum):
        XS = "XS"
        S = "S"
        M = "M"
        L = "L"
        XL = "XL"
        XXL = "XXL"

        @classmethod
        def get_value(cls, member):
            return cls[member].value

    name = models.CharField()
    price = models.DecimalField()
    url = models.URLField()
    description = models.CharField()
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
        ordering = ["headline"]
