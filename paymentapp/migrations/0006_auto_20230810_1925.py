# Generated by Django 3.2.18 on 2023-08-10 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0005_auto_20230809_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='status',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='uid',
        ),
    ]