from django.conf.urls import url

from route.view.route_view import RouteView
from route.view.suggest_detail_view import SuggestDetailView
from route.view.suggest_view import SuggestView

urlpatterns = [
    url(r'^$', RouteView.as_view(), name='index'),
    url(r'^suggest$', SuggestView.as_view(), name='suggest'),
    url(r'^suggest/(?P<hash_id>[\w-]+)', SuggestDetailView.as_view(), name='suggest-detail'),
]
