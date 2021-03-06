# Generated by Django 3.2.9 on 2021-11-10 22:48

from django.db import migrations, models


def insert_variables(apps, schema_editor):
    """
    Copy variable field to variables list
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    CommandsGroupItem = apps.get_model('remotes', 'CommandsGroupItem')
    for item in CommandsGroupItem.objects.exclude(variable__isnull=True):
        item.variables.add(item.variable)
        item.save()

def delete_variables(apps, schema_editor):
    """
    Copy first variable from object to variable
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    CommandsGroupItem = apps.get_model('remotes', 'CommandsGroupItem')
    for item in CommandsGroupItem.objects.exclude(variables__isnull=True):
        item.variable = item.variables.first()
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0040_setting_value_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandsGroupItemVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='order')),
                ('command_group_item', models.ForeignKey(on_delete=models.deletion.PROTECT, to='remotes.commandsgroupitem', verbose_name='command group item')),
                ('variable', models.ForeignKey(on_delete=models.deletion.PROTECT, to='remotes.variable', verbose_name='variable')),
            ],
            options={
                'verbose_name': 'Command group items variable',
                'verbose_name_plural': 'Commands group items variables',
                'ordering': ['command_group_item', 'order', 'variable'],
                'unique_together': {('command_group_item', 'order')},
            },
        ),
        migrations.AddField(
            model_name='commandsgroupitem',
            name='variables',
            field=models.ManyToManyField(blank=True, through='remotes.CommandsGroupItemVariable', to='remotes.Variable', verbose_name='variables'),
        ),
        migrations.RunPython(code=insert_variables,
                             reverse_code=delete_variables),
        migrations.RemoveField(
            model_name='commandsgroupitem',
            name='variable',
        ),
    ]
