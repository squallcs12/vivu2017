from urllib import parse

from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.filter
def replace(var, args):
    """
    Template tag replace string
    @param var: string
    @type var: str
    @param args: "<string>,<replacement>"
    @type args: str
    @return:
    """
    if args is None:
        return False
    old, new = args.split(',')
    return var.replace(old, new)


@register.filter
def is_current_page(request, url_name):
    return request.path == reverse(url_name)


@register.inclusion_tag('general/pagination.html', takes_context=True)
def build_pagination(context, paginator, page_obj):
    request = context['request']
    path = request.path
    get_vars = request.GET.dict()
    if 'page' in get_vars:
        del get_vars['page']

    url = '{}?{}'.format(path, parse.urlencode(get_vars))
    if get_vars:
        url = '{}&'.format(url)

    pages = [-10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10]
    pages = [page_obj.number + x for x in pages]
    max_page_num = paginator.num_pages
    pages = [x for x in pages if 0 < x <= max_page_num]

    return {
        'paginator': paginator,
        'page_obj': page_obj,
        'url': url,
        'pages': pages,
    }
