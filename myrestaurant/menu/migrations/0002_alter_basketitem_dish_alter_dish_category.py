# Generated by Django 5.0.6 on 2024-06-19 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basketitem",
            name="dish",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="menu.dish"
            ),
        ),
        migrations.AlterField(
            model_name="dish",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="dishes",
                to="menu.category",
            ),
        ),
    ]
