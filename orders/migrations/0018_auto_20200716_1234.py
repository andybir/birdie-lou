# Generated by Django 3.0.8 on 2020-07-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_orderitem_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]