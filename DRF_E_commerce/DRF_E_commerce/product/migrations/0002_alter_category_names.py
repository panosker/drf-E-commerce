# Generated by Django 4.2.3 on 2023-08-03 21:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="names",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
