# Generated by Django 3.0.1 on 2020-01-21 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ewardrobe_app', '0012_remove_basket_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='brand_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='color',
            old_name='color',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='retailer',
            old_name='retailer',
            new_name='name',
        ),
    ]