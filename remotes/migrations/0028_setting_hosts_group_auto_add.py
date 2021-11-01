from django.db import migrations

from remotes.constants import HOSTS_GROUP_AUTO_ADD


def insert_settings(apps, schema_editor):
    """
    Insert some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    ALL_HOSTS = 'All hosts'
    Setting = apps.get_model('remotes', 'Setting')
    Setting.objects.create(name=HOSTS_GROUP_AUTO_ADD,
                           description='HostsGroup to automatically add new hosts',
                           value=ALL_HOSTS,
                           is_active=True)
    # Create the All hosts group if it doesn't exist
    HostsGroup = apps.get_model('remotes', 'HostsGroup')
    HostsGroup.objects.get_or_create(name=ALL_HOSTS,
                                     defaults={'is_active': True})

def delete_settings(apps, schema_editor):
    """
    Delete some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    queryset = Setting.objects.filter(name=HOSTS_GROUP_AUTO_ADD)
    queryset.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0027_variable_host_cascade'),
    ]

    operations = [
        migrations.RunPython(code=insert_settings,
                             reverse_code=delete_settings)
    ]
