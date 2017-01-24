from django.views.generic.base import TemplateView

from route.models import Suggest


class SuggestDetailView(TemplateView):
    template_name = 'route/suggest_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SuggestDetailView, self).get_context_data(**kwargs)

        suggest = Suggest.get_by_hash(kwargs['hash_id'])
        related_places = Suggest.objects.filter(province=suggest.province).exclude(pk=suggest.pk)[0:4]

        context.update({
            'suggest': suggest,
            'related_places': related_places
        })
        return context
