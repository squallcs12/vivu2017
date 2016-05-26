import os

from django.conf import settings
from django.http.response import FileResponse


def favicon_view(request):
    fullpath = os.path.join(settings.BASE_DIR, 'common', 'static', 'favicon.ico')
    response = FileResponse(open(fullpath, 'rb'))
    response['content-type'] = 'image/x-icon'
    return response
