# Generated by Django 4.2.11 on 2024-06-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_stock_menu2stock2number"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="phone",
            field=models.CharField(default="", max_length=128),
        ),
    ]
