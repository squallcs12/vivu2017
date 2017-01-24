from django.conf.urls import url

from route.view.suggest_detail_view import SuggestDetailView
from route.view.suggest_view import SuggestView

urlpatterns = [
    url(r'^suggest$', SuggestView.as_view(), name='suggest'),
    url(r'^suggest/(?P<hash_id>[\w-]+)', SuggestDetailView.as_view(), name='suggest-detail'),
]
