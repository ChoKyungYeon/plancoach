# Generated by Django 3.2.18 on 2023-07-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0003_alter_salary_depositor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='accountnumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bank',
            field=models.CharField(blank=True, choices=[('BNK부산은행', 'BNK부산은행'), ('DGB대구은행', 'DGB대구은행'), ('IBK기업은행', 'IBK기업은행'), ('KB국민은행', 'KB국민은행'), ('MG새마을금고', 'MG새마을금고'), ('SC제일은행', 'SC제일은행'), ('Sh수협은행', 'Sh수협은행'), ('광주은행', '광주은행'), ('농협', '농협'), ('신한은행', '신한은행'), ('신협', '신협'), ('우리은행', '우리은행'), ('우체국은행', '우체국은행'), ('저축은행', '저축은행'), ('카카오뱅크', '카카오뱅크'), ('케이뱅크', '케이뱅크'), ('토스', '토스'), ('하나은행', '하나은행')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='depositor',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='given_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]