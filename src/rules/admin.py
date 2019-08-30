# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Rule, TimeBasedRule, FileBasedRule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'content_type',
        'object_id',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = ('content_type', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


    def has_add_permission(self, request):
        return False

@admin.register(TimeBasedRule)
class TimeBasedRuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_date',
        'end_date',
        'action',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'start_date',
        'end_date',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

@admin.register(FileBasedRule)
class FileBasedRuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'supported_format',
        'action',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False
