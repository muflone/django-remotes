from django.db import migrations

from remotes.constants import APILOG_FILTER_USERS


def insert_values(apps, schema_editor):
    """
    Insert some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    Setting.objects.create(name=APILOG_FILTER_USERS,
                           description='List of filtered users in Api logging',
                           value='',
                           is_active=True)

def delete_values(apps, schema_editor):
    """
    Delete some default settings
    """
    # Don't import the Configuration model directly as it may be a newer
    # version than this migration expects.
    Setting = apps.get_model('remotes', 'Setting')
    queryset = Setting.objects.filter(name=APILOG_FILTER_USERS)
    queryset.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0063_setting_apilog_include_arguments'),
    ]

    operations = [
        migrations.RunPython(code=insert_values,
                             reverse_code=delete_values)
    ]
