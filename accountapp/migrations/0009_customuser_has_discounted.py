# Generated by Django 3.2.18 on 2023-10-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0008_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_discounted',
            field=models.BooleanField(default=False),
        ),
    ]
