# Generated by Django 4.1 on 2024-06-14 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("contact_phone", models.CharField(max_length=20)),
            ],
        ),
    ]