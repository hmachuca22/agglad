# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.postgres import fields as pgfields
from django.utils.html import format_html

from jsoneditor.forms import JSONEditor
from mptt.admin import MPTTModelAdmin

from training.utils.admin import CustomBaseAdmin
from .models import (
    Country, State, County, Tag, TrainingUnit, TrainingUnitTag, PublicLink, Area, TrainingCall, Sponsor,
    GeneralConfiguration, Resource, AvatarResource
)


# Inline Classes
# -------------------------------------------------------
class TrainingUnitInlineAdmin(admin.StackedInline):
    model = TrainingUnit
    extra = 0
    fields = [
        'name', 'description', 'content', 'slug', 'order', 'type', 'duration', 'difficulty_level', 'enabled'
    ]
    readonly_fields = ['slug']
    classes = ['collapse']


class TrainingUnitTagInlineAdmin(admin.TabularInline):
    model = TrainingUnitTag
    extra = 0
    fields = ['tag', 'hidden']
    readonly_fields = ['hidden']
    classes = ['collapse']


class StateInlineAdmin(admin.TabularInline):
    model = State
    extra = 0
    fields = ['name', 'code']


class CountyInlineAdmin(admin.TabularInline):
    model = County
    extra = 0
    fields = ['name', 'code']


class SponsorInline(admin.TabularInline):
    model = Sponsor
    extra = 0
    fields = ["organization"]


# Admin classes
# -------------------------------------------------------
class CountryAdmin(CustomBaseAdmin, MPTTModelAdmin):
    list_display = ['id', 'name', 'code']
    list_display_links = ['id', 'name']
    fields = ['name', 'code']
    inlines = [StateInlineAdmin]


class StateAdmin(CustomBaseAdmin, MPTTModelAdmin):
    list_display = ['id', 'name', 'code']
    list_display_links = ['id', 'name']
    fields = ['name', 'code']
    inlines = [CountyInlineAdmin]


class TagAdmin(CustomBaseAdmin):
    list_display = ['id', 'display_name', 'slug']
    list_display_links = ['id', 'display_name']
    fields = ['display_name']


class TrainingUnitAdmin(CustomBaseAdmin, MPTTModelAdmin):
    list_display = ['id', 'name', 'enabled']
    list_display_links = ['id', 'name']
    fields = [
        'name', 'description', 'content', 'slug', 'order', 'type', 'parent', 'duration', 'difficulty_level', 'enabled'
    ]
    readonly_fields = ['slug']
    inlines = [TrainingUnitTagInlineAdmin, TrainingUnitInlineAdmin]


class TrainingCallAdmin(CustomBaseAdmin):
    fields = [
        'training_plan', 'status', 'type', 'enrollment_start_date', 'enrollment_end_date', 'start_date', 'end_date',
        'slug', 'banner', 'thumbnail_banner'
    ]
    list_display = ["id", "status"]
    list_display_links = ["id"]
    inlines = [SponsorInline]


class ResourceAdmin(CustomBaseAdmin):
    formfield_overrides = {pgfields.JSONField: {"widget": JSONEditor}}

    def asset_preview(self, obj):
        if obj:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="75" /></a>', obj.asset.url, obj.asset.url
            )
        else:
            return 'No disponible'
    asset_preview.short_description = "Preview"


class AvatarResourceAdmin(ResourceAdmin):
    fields = ["name", "type", "asset", "extra_data"]
    list_display = ["id", "name", "gender", "asset_preview"]
    list_display_links = ["id", "name"]


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TrainingUnit, TrainingUnitAdmin)
admin.site.register(PublicLink)
admin.site.register(Area)
admin.site.register(GeneralConfiguration)
admin.site.register(TrainingCall, TrainingCallAdmin)
admin.site.register(AvatarResource, AvatarResourceAdmin)
