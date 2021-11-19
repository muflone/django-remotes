# Generated by Django 3.2.9 on 2021-11-14 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0051_commands_group_item_command'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commandsgroupitem',
            old_name='command_text',
            new_name='command',
        ),
        migrations.AlterModelOptions(
            name='commandsgroupitem',
            options={'ordering': ['group', 'order', '-is_active'], 'verbose_name': 'Commands group item', 'verbose_name_plural': 'Commands group items'},
        ),
        migrations.AlterField(
            model_name='commandsgroupitem',
            name='command',
            field=models.TextField(default=None, verbose_name='command'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Command',
        ),
    ]