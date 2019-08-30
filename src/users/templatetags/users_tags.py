from django import template
from django.contrib.auth import get_user_model
register = template.Library()


USER = get_user_model()

@register.simple_tag(takes_context=True)
def get_unknown_users(context=True):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    return USER.objects.filter(client__isnull=True) if user.is_staff \
        else USER.objects.none()