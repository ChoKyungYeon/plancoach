# Generated by Django 3.2.18 on 2023-12-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_subjectapp', '0002_alter_profile_subject_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_subject',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
