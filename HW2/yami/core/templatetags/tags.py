from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    _dict = context['request'].GET.copy()
    _dict.update(kwargs)
    return urlencode(_dict)
