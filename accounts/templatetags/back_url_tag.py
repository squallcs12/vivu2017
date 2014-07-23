'''
Created on Jul 29, 2013

@author: antipro
'''
from django import template
from django.contrib.auth import REDIRECT_FIELD_NAME
from common.django_custom import get_go_back_url

register = template.Library()

css_files = []
js_files = []

@register.tag
def back_url(parser, token):
    try:
        tag_name, default = token.split_contents()  # @UnusedVariable
        return BackUrlNode(default=default)
    except ValueError:
        return BackUrlNode()

class BackUrlNode(template.Node):
    def __init__(self, default=None, redirect_field_name=REDIRECT_FIELD_NAME):
        self._default = default
        self._redirect_field_name = redirect_field_name

    def render(self, context):
        request = context['request']
        backUrl = get_go_back_url(request, self._redirect_field_name, self._default)
        return '' if not backUrl else '?next=%s' % backUrl
