from django import template
from donghu.models import Module

register = template.Library()

@register.inclusion_tag('donghu/nav.html')
def get_nav_list(mod=None, user=None):
    return {'mods': Module.objects.all(),
            'act_mod': mod,
            'user': user}