from django.contrib import admin

from .models import Question, Choice, Voter
from .models import Module, Article

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Voter)
admin.site.register(Module)
admin.site.register(Article)

admin.site.site_header = '东湖论坛'
admin.site.site_title = 'DonghuBBS'