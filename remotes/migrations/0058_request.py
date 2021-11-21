# Generated by Django 3.2.9 on 2021-11-21 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remotes', '0057_command_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('remote_address', models.CharField(max_length=255, verbose_name='remote address')),
                ('method', models.CharField(max_length=255, verbose_name='method')),
                ('path_info', models.CharField(max_length=255, verbose_name='path info')),
                ('querystring', models.TextField(blank=True, verbose_name='query string')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
                'ordering': ['timestamp', 'id'],
            },
        ),
    ]
