# Generated by Django 3.2.7 on 2021-10-20 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0015_commands_output'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandsgroup',
            name='after',
            field=models.DateTimeField(verbose_name='after'),
        ),
        migrations.AlterField(
            model_name='commandsgroup',
            name='before',
            field=models.DateTimeField(verbose_name='before'),
        ),
    ]