# Generated by Django 3.0.8 on 2020-07-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20200716_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
