# Generated by Django 3.2.9 on 2021-11-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0064_setting_apilog_filter_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandvariable',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='order'),
        ),
        migrations.AlterUniqueTogether(
            name='commandvariable',
            unique_together={('command', 'order', 'variable')},
        ),
    ]
