# Generated by Django 3.2.7 on 2021-10-09 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0005_variable_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('raw_value', models.TextField(blank=True, verbose_name='value')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='remotes.host', verbose_name='host')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='remotes.variabletype', verbose_name='type')),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
                'ordering': ['host', 'name'],
                'unique_together': {('host', 'name')},
            },
        ),
    ]
