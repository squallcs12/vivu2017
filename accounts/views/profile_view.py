from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from accounts.forms import UserForm


class EditProfileView(FormView):
    template_name = "accounts/edit_profile.html"
    form_class = UserForm
    success_url = reverse_lazy('accounts:profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(EditProfileView, self).get_form_kwargs()
        form_kwargs.update(instance=self.request.user)
        return form_kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('User profile has been saved.'))
        return super(EditProfileView, self).form_valid(form)


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"
    editable = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'active_profile': True,
            'editable': self.editable,
        })

        return context
