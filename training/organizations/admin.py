# -*- coding: utf-8 -*-
from django.contrib import admin

from training.utils.admin import CustomBaseAdmin

from training.users.models import OrganizationalProfile
from .models import Organization


# Inline Classes
# -------------------------------------------------------
class OrganizationalProfileInlineAdmin(admin.TabularInline):
    model = OrganizationalProfile
    extra = 0
    fields = ["user"]
    classes = ['collapse']


# Admin classes
# -------------------------------------------------------
class OrganizationAdmin(CustomBaseAdmin):
    list_display = ['id', 'name', 'code', 'type']
    list_display_links = ['id', 'name']
    fields = ['name', 'code', 'type']
    list_filter = ['type']

    inlines = [OrganizationalProfileInlineAdmin,]


admin.site.register(Organization, OrganizationAdmin)
