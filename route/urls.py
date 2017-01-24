from django.conf.urls import url

from route.view.suggest_view import SuggestView

urlpatterns = [
    url(r'^suggest', SuggestView.as_view(), name='suggest'),
]
