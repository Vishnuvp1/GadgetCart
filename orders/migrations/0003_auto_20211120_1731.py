# Generated by Django 3.1 on 2021-11-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]