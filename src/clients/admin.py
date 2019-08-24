# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Client, ClientAgent


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_active',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = ('is_active', 'created_at', 'updated_at', 'deleted_at')
    filter_horizontal = ('parser',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(ClientAgent)
class ClientAgentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'name',
        'email',
        'is_logged_allowed',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'client',
        'is_logged_allowed',
        'created_at',
        'updated_at',
        'deleted_at',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
