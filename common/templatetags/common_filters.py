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
