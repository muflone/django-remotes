# Generated by Django 3.2.7 on 2021-10-30 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0026_commands_output_host_cascade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remotes.host', verbose_name='host'),
        ),
    ]
