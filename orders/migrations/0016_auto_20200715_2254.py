# Generated by Django 3.0.8 on 2020-07-16 02:54

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20200713_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=django_countries.fields.CountryField(default=['US'], max_length=100),
        ),
    ]
