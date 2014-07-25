'''
Created on Sep 18, 2013

@author: antipro
'''
from django.template.response import TemplateResponse
from django.views.generic.base import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from accounts.forms import UserForm


class EditProfileView(UpdateView):
    template = "accounts/edit_profile.html"

    def _render(self, request, **kwargs):
        data = {}
        data['active_profile'] = True

        data.update(**kwargs)
        return TemplateResponse(request, self.template, data)

    @method_decorator(login_required)
    def get(self, request):
        profile_form = UserForm(instance=request.user.get_profile())

        return self._render(request, profile_form=profile_form)

    @method_decorator(login_required)
    def post(self, request):
        profile_form = UserForm(request.POST, instance=request.user.get_profile())

        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts_profile')
        else:
            return self._render(request, profile_form=profile_form)


class ProfileView(View):
    template = "accounts/profile.html"
    editable = False

    @method_decorator(login_required)
    def get(self, request):
        data = {}
        data['user'] = request.user
        data['profile'] = request.user
        data['active_profile'] = True

        if self.editable:
            data['editable'] = self.editable
        else:
            pass

        return TemplateResponse(request, self.template, data)

