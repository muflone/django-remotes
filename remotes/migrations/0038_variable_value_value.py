# Generated by Django 3.2.9 on 2021-11-09 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0037_command_variables'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variablevalue',
            old_name='raw_value',
            new_name='value',
        ),
    ]