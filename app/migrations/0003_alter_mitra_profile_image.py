# Generated by Django 4.2.6 on 2023-11-05 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_member_user_type_remove_mitra_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mitra',
            name='profile_image',
            field=models.ImageField(blank=True, default='mitra/default-logo.png', null=True, upload_to='mitra/'),
        ),
    ]
