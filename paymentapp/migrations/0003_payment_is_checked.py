# Generated by Django 3.2.18 on 2023-07-23 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0002_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_checked',
            field=models.PositiveIntegerField(default=False),
        ),
    ]