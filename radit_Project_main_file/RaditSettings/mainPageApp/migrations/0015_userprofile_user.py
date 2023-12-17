# Generated by Django 5.0 on 2023-12-15 06:45

import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPageApp', '0014_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.expressions.Case, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]