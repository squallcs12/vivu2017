from django.conf.urls import url

from blog.views.post_view import PostView

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)\.html', PostView.as_view(), name='post'),
]
