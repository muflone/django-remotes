# Generated by Django 3.2.9 on 2021-11-09 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0038_variable_value_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='value'),
        ),
    ]
