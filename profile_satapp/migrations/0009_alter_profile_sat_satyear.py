# Generated by Django 3.2.18 on 2023-12-08 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_satapp', '0008_alter_profile_sat_satverificationimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_sat',
            name='satyear',
            field=models.IntegerField(choices=[(9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)]),
        ),
    ]