# Generated by Django 3.1 on 2021-11-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211125_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(max_length=100),
        ),
    ]