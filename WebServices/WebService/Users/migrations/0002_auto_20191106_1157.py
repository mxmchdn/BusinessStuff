# Generated by Django 2.2.7 on 2019-11-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='profile',
            name='powerbi',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
