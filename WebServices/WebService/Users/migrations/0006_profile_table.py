# Generated by Django 2.2.7 on 2019-11-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20191106_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='table',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
