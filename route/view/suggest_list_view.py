from django.conf import settings
from django.views.generic.list import ListView

from route.forms import SuggestFilterForm
from route.models import Suggest


class SuggestListView(ListView):
    queryset = Suggest.objects.filter(is_approved=True).exclude(is_chosen=True)
    context_object_name = 'suggests'
    paginate_by = settings.ROUTE_SUGGEST_LIST_PAGE_SIZE

    def get_queryset(self):
        queryset = super(SuggestListView, self).get_queryset()
        province = self.request.GET.get('province')
        if province:
            queryset = queryset.filter(province=province)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SuggestListView, self).get_context_data(**kwargs)
        context.update({
            'filter_form': SuggestFilterForm(data=self.request.GET),
        })

        return context
