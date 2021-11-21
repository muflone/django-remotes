from django.db import migrations

from remotes.constants import APILOG_ENABLE_LOGGING


def insert_values(apps, schema_editor):
    """
    Insert some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    Setting.objects.create(name=APILOG_ENABLE_LOGGING,
                           description='Enable Api logging',
                           value='0',
                           is_active=True)

def delete_values(apps, schema_editor):
    """
    Delete some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    queryset = Setting.objects.filter(name=APILOG_ENABLE_LOGGING)
    queryset.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0061_apilog'),
    ]

    operations = [
        migrations.RunPython(code=insert_values,
                             reverse_code=delete_values)
    ]
