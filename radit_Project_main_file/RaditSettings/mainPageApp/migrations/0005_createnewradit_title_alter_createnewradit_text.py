# Generated by Django 5.0 on 2023-12-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPageApp', '0004_reviewsaboutsite_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='createnewradit',
            name='title',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='createnewradit',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]
