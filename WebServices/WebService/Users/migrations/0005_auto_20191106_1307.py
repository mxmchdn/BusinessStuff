# Generated by Django 2.2.7 on 2019-11-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='Grant-Thornton-Default.jpeg', upload_to='profile_img'),
        ),
    ]