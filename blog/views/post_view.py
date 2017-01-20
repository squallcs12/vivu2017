from django.views.generic.detail import DetailView

from blog.models import Post


class PostView(DetailView):
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context.update({
            'absolute_url': self.request.build_absolute_uri(self.get_object().get_absolute_url()),
            'webpush': {
                'group': 'blog_post',
            },
        })
        return context
