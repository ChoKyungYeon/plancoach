# Generated by Django 3.2.18 on 2023-07-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_planapp', '0003_feedback_plan_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback_plan',
            name='content',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]