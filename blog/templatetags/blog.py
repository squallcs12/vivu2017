from django import template

register = template.Library()


@register.inclusion_tag('blog/post.html', takes_context=True)
def render_post(context, post):
    request = context['request']
    return {
        'post': post,
        'request': request,
        'absolute_url': request.build_absolute_uri(post.get_absolute_url()),
    }
