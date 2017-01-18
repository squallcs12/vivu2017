from django.conf import settings
from django.views.generic.base import TemplateView

from blog.models import Post
from progress.models import Progress


class HomeView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'planing_progress': Progress.objects.filter(id=settings.HEADER_PROGRESS_ID).first(),
            'header_post': Post.objects.filter(id=settings.HEADER_POST_ID).first(),
        })
        return context
