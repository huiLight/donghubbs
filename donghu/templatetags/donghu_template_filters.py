from django import template

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