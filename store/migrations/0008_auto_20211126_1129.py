# Generated by Django 3.1 on 2021-11-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("store", "0007_auto_20211126_1127")]

    operations = [
        migrations.AlterField(
            model_name="variation",
            name="variation_category",
            field=models.CharField(choices=[("color", "color")], max_length=100),
        )
    ]
