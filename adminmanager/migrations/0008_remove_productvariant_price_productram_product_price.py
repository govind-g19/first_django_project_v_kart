# Generated by Django 5.0 on 2024-01-08 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmanager', '0007_productcolor_productram_productrom_productvariant_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='price',
        ),
        migrations.AddField(
            model_name='productram',
            name='product_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
