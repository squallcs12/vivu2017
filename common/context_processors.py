import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.urls.base import reverse
from django.utils.translation import ugettext as _


def site_name(request):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        name = Site.objects.get(pk=settings.SITE_ID).name
    else:
        name = settings.SITE_NAME
    return {'SITE_NAME': name}


def django_settings(request):
    keys = [
        'LOGIN_URL',
        'LOGOUT_URL',
        'FACEBOOK_APP_ID',
        'GOOGLE_MAP_API_KEY',
    ]

    return {x: getattr(settings, x) for x in keys}


def nav_links(request):
    links = [{
        'href': reverse('index'),
        'text': _('Trang chủ'),
        'class': 'active',
    }, {
        'href': reverse('route:suggest'),
        'text': _('Lịch trình'),
        'patterns': [
            r'^/route',
        ],
    }]

    for link in links[1:]:
        if any(re.match(x, request.path) for x in link['patterns']):
            link['class'] = 'active'
            links[0]['class'] = ''  # deactivate home
            break

    return {'nav_links': links}
