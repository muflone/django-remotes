from django.db import migrations

from remotes.constants import SERVER_URL


def insert_settings(apps, schema_editor):
    """
    Insert some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    Setting.objects.create(name=SERVER_URL,
                           description='Server URL',
                           value='http://YOUR_SERVER:8000',
                           is_active=True)

def delete_settings(apps, schema_editor):
    """
    Delete some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    queryset = Setting.objects.filter(name=SERVER_URL)
    queryset.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0001_setting'),
    ]

    operations = [
        migrations.RunPython(code=insert_settings,
                             reverse_code=delete_settings)
    ]
