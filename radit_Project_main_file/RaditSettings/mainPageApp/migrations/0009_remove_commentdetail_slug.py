# Generated by Django 5.0 on 2023-12-11 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainPageApp', '0008_commentdetail_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentdetail',
            name='slug',
        ),
    ]