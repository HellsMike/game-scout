# Generated by Django 4.0 on 2022-05-01 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0033_alter_product_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_seller_rated',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
