# Generated by Django 5.0 on 2023-12-27 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='solid_out',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
