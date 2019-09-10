# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ParserConfigurationDef, \
    ColumnPayloadMap, ParserCollection, PostIngestion




class ColumnPayloadMapAdmin(admin.TabularInline):
    model = ColumnPayloadMap
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


@admin.register(ParserConfigurationDef)
class ParserConfigurationDefAdmin(admin.ModelAdmin):
    inlines = [ColumnPayloadMapAdmin, ]
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

@admin.register(ParserCollection)
class ParserCollection(admin.ModelAdmin):
    pass



@admin.register(PostIngestion)
class ParserCollection(admin.ModelAdmin):
    pass


