# Generated by Django 2.2.7 on 2019-11-06 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20191106_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='exeution_left',
            new_name='execution_left',
        ),
    ]