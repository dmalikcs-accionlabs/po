# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import IngestionData, IngestionDataAttachment


class IngestionDataAttachmentAdmin(admin.TabularInline):
    model = IngestionDataAttachment
    list_display = (
        'id',
        'ingestion',
        'name',
        'f_format',
        'is_supported',
        'data_file',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'ingestion',
        'is_supported',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(IngestionData)
class IngestionDataAdmin(admin.ModelAdmin):
    inlines = [IngestionDataAttachmentAdmin, ]
    list_display = (
        'id',
        'agent',
        'subject',
        'body',
        'can_process',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'agent',
        'can_process',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    date_hierarchy = 'updated_at'

    def has_add_permission(self, request):
        return True if request.user.is_superuser else False

