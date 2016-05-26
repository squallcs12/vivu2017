from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from social.apps.django_app.default import models

@login_required
def main(request, template='accounts/social.html'):
    data = {}

    socials = models.UserSocialAuth.objects.filter(user=request.user)
    data['socials'] = socials

    return TemplateResponse(request, template, data)


