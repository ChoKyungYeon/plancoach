# Generated by Django 3.2.18 on 2024-02-10 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_careerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_career',
            name='year',
            field=models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)]),
        ),
    ]
