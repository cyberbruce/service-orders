# Generated by Django 5.1.1 on 2024-10-06 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_alter_order_order_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.CharField(blank=True, default="", max_length=50, unique=True),
        ),
    ]
