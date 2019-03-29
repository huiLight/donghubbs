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
    ]

    python_article = [
        {"module": "interests", "title": "我在1", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在2", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在3", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在4", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在5", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在6", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在7", "author": 19, "content": "我思故我在。"},
        {"module": "interests", "title": "我在8", "author": 19, "content": "我思故我在。"},
    ]

    python_chats = [
        {"title": "我在9", "content": "我思故我在。"},
        {"title": "okok1", "content":"kkkkkkkkk"},
        {"title": "我在0", "content": "我思故我在。"},
        {"title": "okok2", "content":"kkkkkkkkk"},
        {"title": "我在a", "content": "我思故我在。"},
        {"title": "okok3", "content":"kkkkkkkkk"},
        {"title": "我在b", "content": "我思故我在。"},
        {"title": "okok4", "content":"kkkkkkkkk"},
        {"title": "我在c", "content": "我思故我在。"},
        {"title": "okok5", "content":"kkkkkkkkk"},
        {"title": "我在d", "content": "我思故我在。"},
        {"title": "okok6", "content":"kkkkkkkkk"},
        {"title": "我在e", "content": "我思故我在。"},
        {"title": "okok7", "content":"kkkkkkkkk"},
        {"title": "我在f", "content": "我思故我在。"},
        {"title": "okok8", "content":"kkkkkkkkk"},
        {"title": "我在g", "content": "我思故我在。"},
        {"title": "okok9", "content":"kkkkkkkkk"},
        {"title": "我在h", "content": "我思故我在。"},
        {"title": "okok0", "content":"kkkkkkkkk"},
    ]   

    commentary = [
        {"content":"okokokokokokokokokok"},
    ]

    cats = {
        "interests": python_article,
        "chats": python_chats,
    }
    for i in python_modules:
        add_module(i["name"], i["name_zh"])

    # for i in python_article:
    #     add_article(i['title'], i['content'])

    author = User.objects.get(username='root')
    for m, i in cats.items():
        module = Module.objects.get(name=m)
        for a in i:
            ar = add_article(module, a['title'], author, a['content'])
            c = Commentary.objects.get_or_create(article=ar, author=author, content='okok')[0]
            c.save()

def add_module(name, name_zh):
    c = Module.objects.get_or_create(name=name, name_zh=name_zh)[0]
    c.save()
    return c

def add_article(module,title, author, content):
    a = Article.objects.get_or_create(module=module, title=title, author=author, content=content)[0]
    a.save()
    return a


if __name__ == '__main__':
    print('-------------start-------------')
    init()
    print('--------------end--------------')
