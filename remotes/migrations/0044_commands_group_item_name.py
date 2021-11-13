# Generated by Django 3.2.9 on 2021-11-13 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0043_command_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commandsgroupitem',
            options={'ordering': ['group', 'order', '-is_active', 'command'], 'verbose_name': 'Commands group item', 'verbose_name_plural': 'Commands group items'},
        ),
        migrations.AlterUniqueTogether(
            name='commandsgroupitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='commandsgroupitem',
            name='name',
        ),
    ]
