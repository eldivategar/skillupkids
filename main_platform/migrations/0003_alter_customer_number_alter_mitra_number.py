# Generated by Django 4.2.6 on 2023-10-17 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_platform', '0002_alter_customer_number_alter_mitra_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='number',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='mitra',
            name='number',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
