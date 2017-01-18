from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/post.html', takes_context=True)
def render_post(context, post):
    if isinstance(post, str):
        post = Post.objects.filter(slug=post).first()
    if not post:
        return
    request = context['request']
    return {
        'post': post,
        'request': request,
        'absolute_url': request.build_absolute_uri(post.get_absolute_url()),
    }
