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

from donghu.models import Module, Article, Commentary
from django.contrib.auth.models import User

def init():
    python_modules = [
        {"name":'interests', "name_zh": '兴趣爱好'},
        {"name":'activities', "name_zh": '活动比赛'},
        {"name":'chats', "name_zh": '谈天说地'},
        {"name":'jobs', "name_zh": '兼职招聘'},
        {"name":'experiencing', "name_zh": '你问我答'},
        {"name":'lost', "name_zh": '失物招领'},
        {"name":'resources', "name_zh": '资源共享'},
        {"name":'vote', "name_zh":'投票'},        
    ]

    for i in python_modules:
        add_module(i["name"], i["name_zh"])


def add_module(name, name_zh):
    c = Module.objects.get_or_create(name=name, name_zh=name_zh)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('-------------start-------------')
    init()
    print('--------------end--------------')
