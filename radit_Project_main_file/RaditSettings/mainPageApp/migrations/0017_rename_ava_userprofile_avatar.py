# Generated by Django 5.0 on 2023-12-15 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainPageApp', '0016_alter_userprofile_ava'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='ava',
            new_name='avatar',
        ),
    ]
