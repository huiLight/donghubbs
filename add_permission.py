import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'donghubbs.settings')
"""
When importing Django models, make sure you have imported your project’s settings
by importing django and setting the environment variable DJANGO_SETTINGS_MODULE
to be your project’s setting file, as demonstrated in lines 1 to 6 above. You then call
django.setup() to import your Django project’s settings.
"""
import django
django.setup()

from donghu.models import Module
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType

'''
    为每个板块增加相应的权限
'''
def add_permissions():
    content_type = ContentType.objects.get_for_model(Module)
    for i in Module.objects.all():
        permission = Permission.objects.get_or_create(
            codename='have_permission_'+i.name,
            name='have permission '+i.name,
            content_type=content_type,
        )

# 添加组，并且为每个组添加相应的权限
def add_groups():
    for i in Module.objects.all():
        permission = Permission.objects.get(codename='have_permission_'+i.name)
        g = Group.objects.get_or_create(name=i.name)[0] # 返回一个元组，在这里取元组中第一个元素
        g.permissions.add(permission)

if __name__ == '__main__':
    add_permissions()
    add_groups()