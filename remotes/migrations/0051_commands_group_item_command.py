# Generated by Django 3.2.9 on 2021-11-14 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0050_commands_group_item_command_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandsgroupitem',
            name='command',
        ),
    ]
