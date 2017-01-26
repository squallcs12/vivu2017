from django.views.generic.base import TemplateView

from route.models import Suggest


class RouteView(TemplateView):
    template_name = 'route/index.html'

    def get_context_data(self, **kwargs):
        context = super(RouteView, self).get_context_data(**kwargs)
        context.update({
            'top_suggests': Suggest.objects.exclude(chosen=True)[0:4],
            'chosen_places': Suggest.objects.filter(chosen=True),
        })
        return context

