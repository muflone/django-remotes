from django.db import migrations

from remotes.constants import APILOG_INCLUDE_ARGS


def insert_values(apps, schema_editor):
    """
    Insert some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    Setting.objects.create(name=APILOG_INCLUDE_ARGS,
                           description='Include arguments in Api logging',
                           value='0',
                           is_active=True)

def delete_values(apps, schema_editor):
    """
    Delete some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    queryset = Setting.objects.filter(name=APILOG_INCLUDE_ARGS)
    queryset.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0062_setting_apilog_enable_logging'),
    ]

    operations = [
        migrations.RunPython(code=insert_values,
                             reverse_code=delete_values)
    ]
