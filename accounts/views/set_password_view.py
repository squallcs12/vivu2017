'''
Created on Aug 26, 2013

@author: antipro
'''
from django.contrib.auth.views import password_change
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@login_required
def main(request):
    if request.user.has_usable_password():
        return HttpResponseRedirect(reverse('password_change'))
    return password_change(request,
                           template_name='accounts/password_set.html',
                           password_change_form=SetPasswordForm,
                           post_change_redirect=reverse('password_set_done'))


def done(request, template='accounts/password_set_done.html'):
    data = {}
    return TemplateResponse(request, template, data)
