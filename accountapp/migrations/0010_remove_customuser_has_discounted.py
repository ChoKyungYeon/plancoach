# Generated by Django 3.2.18 on 2023-10-18 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0009_customuser_has_discounted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='has_discounted',
        ),
    ]