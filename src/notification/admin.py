# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import TextNotification


@admin.register(TextNotification)
class TextNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reference_content_type',
        'reference_object_id',
        'content_type',
        'object_id',
        'cnt_code',
        'contact_number',
        'msg',
        'is_dispatched',
        'is_delivered',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'reference_content_type',
        'content_type',
        'is_dispatched',
        'is_delivered',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    date_hierarchy = 'created_at'
