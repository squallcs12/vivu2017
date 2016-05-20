from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from accounts.forms import UserForm


class EditProfileView(FormView):
    template = "accounts/edit_profile.html"
    form_class = UserForm
    success_url = reverse_lazy('accounts:profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        return form_class(instance=self.request.user)

    def form_valid(self, form):
        form.save()
        return super(EditProfileView, self).form_valid(form)


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"
    editable = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'active_profile': True,
            'editable': self.editable,
        })
