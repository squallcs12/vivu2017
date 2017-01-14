from django.conf import settings


def site_name(request):
    return {'SITE_NAME': settings.SITE_NAME}


def django_settings(request):
    keys = [
        'LOGIN_URL',
        'LOGOUT_URL',
    ]

    return {x: getattr(settings, x) for x in keys}
