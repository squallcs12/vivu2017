from django.http.response import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from route.models import Suggest
from route.services.suggest_like import SuggestLike


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

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SuggestDetailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, hash_id):
        suggest_id = Suggest.get_id_from_hash(hash_id)
        if not suggest_id:
            raise Http404()

        SuggestLike.add_id(suggest_id)

        return HttpResponse()
