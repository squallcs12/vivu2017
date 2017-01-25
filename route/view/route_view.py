from django.views.generic.base import TemplateView

from route.models import Suggest


class RouteView(TemplateView):
    template_name = 'route/index.html'

    def get_context_data(self, **kwargs):
        context = super(RouteView, self).get_context_data(**kwargs)
        context.update({
            'top_suggests': Suggest.objects.all()[0:4]
        })
        return context
