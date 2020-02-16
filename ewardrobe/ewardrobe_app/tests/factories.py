import factory
from django.contrib.auth.models import User

from ewardrobe_app import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "john_%s" % n)
    email = factory.LazyAttribute(lambda o: "%s@example.com" % o.username)
    password = factory.Sequence(lambda n: "password%s" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    name = "brand"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = "category"


class RetailerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Retailer

    name = "retailer"


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Color

    name = "color"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: "test_product_%s" % n)
    price = factory.Sequence(lambda n: n)
    url = factory.LazyAttribute(lambda o: "%s@example.com" % o.name)
    description = factory.Sequence(lambda n: "test_product_description_%s" % n)
    rating = factory.Sequence(lambda n: n)
    review_count = factory.Sequence(lambda n: n)
    brand = factory.SubFactory(BrandFactory)
    product_category = factory.SubFactory(CategoryFactory)
    retailer = factory.SubFactory(RetailerFactory)
    color = factory.SubFactory(ColorFactory)
