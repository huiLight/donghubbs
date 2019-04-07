from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def transform(value):
    '''
    转换浏览人数的显示方式
    '''
    if value >= 10000:
        result = '10k+'
    elif value >= 1000:
       result = '{0:.1f}k'.format(value / 1000)
    else:
        result = value
    return result

@register.filter
def has_permission(user, category):
    # 不要忘记加 donghu. ,用户只拥有该应用下的权限
    return user.has_perm('donghu.have_permission_'+category)