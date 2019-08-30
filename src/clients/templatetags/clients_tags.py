from django import template

register = template.Library()

from clients.models import Client, ClientAgent

@register.simple_tag(takes_context=True)
def get_client_count(context):
    request = context['request']
    if not request.user.is_authenticated:
        return
    return Client.objects.\
        filter(deleted_at__isnull=True).count() \
        if request.user.is_staff else 0


@register.simple_tag(takes_context=True)
def get_agent_count(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    return ClientAgent.objects.\
        filter(deleted_at__isnull=True).count() \
        if user.is_staff else 0


@register.simple_tag(takes_context=True)
def get_action_required_agent(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return ClientAgent.objects.none()
    return ClientAgent.objects.\
        filter(deleted_at__isnull=True, client__isnull=True) \
        if user.is_staff else ClientAgent.objects.none()
