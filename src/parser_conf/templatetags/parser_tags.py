from django import template

register = template.Library()

from parser_conf.models import ParserConfigurationDef

@register.simple_tag(takes_context=True)
def get_parser_count(context):
    req = context['request']
    u = req.user
    if not u.is_authenticated:
        return

    return ParserConfigurationDef.objects. \
        filter(deleted_at__isnull=True).count() if u.is_staff else \
        ParserConfigurationDef.objects.filter(deleted_at__isnull=True, user=u).count()


@register.simple_tag(takes_context=True)
def get_parsers(context):
    req = context['request']
    u = req.user
    if not u.is_authenticated:
        return

    return ParserConfigurationDef.objects. \
        filter(deleted_at__isnull=True) if u.is_staff else \
        ParserConfigurationDef.objects.filter(deleted_at__isnull=True, user=u)