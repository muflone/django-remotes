# Generated by Django 3.2.9 on 2021-11-08 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0035_variable_value_variable'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='category',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='category'),
        ),
    ]
