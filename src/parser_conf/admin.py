# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ParserConfigurationDef, ColumnPayloadMap


@admin.register(ParserConfigurationDef)
class ParserConfigurationDefAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'f_format',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(ColumnPayloadMap)
class ColumnPayloadMapAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'config',
        'column_name',
        'payload',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = ('config', 'created_at', 'updated_at', 'deleted_at')
    date_hierarchy = 'created_at'
