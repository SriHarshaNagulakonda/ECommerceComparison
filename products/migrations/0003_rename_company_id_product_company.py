# Generated by Django 4.2.8 on 2023-12-14 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='company_id',
            new_name='company',
        ),
    ]