# Generated by Django 3.2.7 on 2021-10-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0023_command_timeout'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
    ]