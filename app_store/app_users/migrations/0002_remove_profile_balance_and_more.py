# Generated by Django 5.0.2 on 2024-03-08 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="balance",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="purchase_amount",
        ),
    ]