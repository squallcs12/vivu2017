from django.conf import settings
from django.contrib.sites.models import Site


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
    ]

    return {x: getattr(settings, x) for x in keys}
