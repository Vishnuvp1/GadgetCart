# Generated by Django 3.1 on 2021-12-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("brand", "0004_brand_created_at")]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        )
    ]
