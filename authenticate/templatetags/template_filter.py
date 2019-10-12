from django.template import Library

register = Library()


@register.filter
def is_admin(arg):
    return arg.groups.filter(name="ADMIN").exists()
