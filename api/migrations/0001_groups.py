from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from rest_framework.authtoken.models import Token

from remotes.constants import (PERMISSION_CAN_REGISTER_HOSTS,
                               USER_GROUP_REGISTER_HOSTS)

USER_REGISTER_HOST = 'user_register_hosts'


def insert_users(apps, schema_editor):
    """
    Insert some default users and groups
    """
    User = get_user_model()
    # New Permissions
    content_type = ContentType.objects.get_for_model(User)
    new_permission = Permission.objects.create(
        codename=PERMISSION_CAN_REGISTER_HOSTS,
        name='Can register new hosts',
        content_type=content_type)
    # Add User
    new_user = User.objects.create(username=USER_REGISTER_HOST,
                                   first_name='Register',
                                   last_name='Hosts',
                                   is_active=True)
    # Add Token
    Token.objects.create(user=new_user)
    # Add Group
    Group = apps.get_model('auth', 'Group')
    new_group = Group.objects.create(name=USER_GROUP_REGISTER_HOSTS)
    new_group.user_set.add(new_user.pk)
    new_group.permissions.add(new_permission.pk)
    new_group.save()

def delete_users(apps, schema_editor):
    """
    Delete some default users and groups
    """
    User = get_user_model()
    queryset = User.objects.filter(username=USER_REGISTER_HOST)
    queryset.delete()
    Group = apps.get_model('auth', 'Group')
    queryset = Group.objects.filter(name=USER_GROUP_REGISTER_HOSTS)
    queryset.delete()
    queryset = Permission.objects.filter(codename=PERMISSION_CAN_REGISTER_HOSTS)
    queryset.delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('remotes', '0027_variable_host_cascade'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authtoken', '0003_tokenproxy'),
    ]

    operations = [
        migrations.RunPython(code=insert_users,
                             reverse_code=delete_users),
    ]
