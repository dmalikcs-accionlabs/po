from django import template

register = template.Library()

from ingestion.models import IngestionData,\
    IngestionDataAttachment
from ingestion.choices import StatusChoice

@register.simple_tag(takes_context=True)
def get_ingestion_count(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    q = IngestionData.objects. \
        filter(deleted_at__isnull=True)
    return q.count() if user.is_staff else user.ingestions.filter(deleted_at__isnull=True).count()


@register.simple_tag(takes_context=True)
def get_failed_ingestion_count(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    q = IngestionData.objects. \
        filter(deleted_at__isnull=True, status=StatusChoice.COMPLETED_FAILED)
    return q.count() if user.is_staff else q.filter(user=user).count()


@register.simple_tag(takes_context=True)
def get_success_ingestion_count(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    q = IngestionData.objects. \
        filter(deleted_at__isnull=True, status=StatusChoice.COMPLETED_SUCCESS)
    return q.count() if user.is_staff else q.filter(user=user).count()


@register.simple_tag(takes_context=True)
def get_recent_ingestions(context):
    request = context['request']
    user = request.user
    if not user.is_authenticated:
        return
    q = IngestionData.objects. \
               filter(deleted_at__isnull=True)
    return q.order_by('-created_at')[:15] if user.is_staff \
        else q.filter(user=user).order_by('-created_at')[:15]


@register.simple_tag(takes_context=True)
def load_inventory(context, id):
    i = IngestionDataAttachment.object.get(pk=id)

    return i.get_inventory()