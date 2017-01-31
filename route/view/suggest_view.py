from django.views.generic.base import TemplateView


class SuggestView(TemplateView):
    template_name = 'route/suggest.html'
