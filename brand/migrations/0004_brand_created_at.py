# Generated by Django 3.1 on 2021-12-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("brand", "0003_remove_brand_stock")]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        )
    ]
