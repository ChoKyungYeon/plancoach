# Generated by Django 3.2.18 on 2023-12-10 16:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profile_consulttypeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_consulttype',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
