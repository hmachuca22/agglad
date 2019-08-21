# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.postgres import fields as pgfields

from jsoneditor.forms import JSONEditor

from training.utils.admin import CustomBaseAdmin
from .models import TrainingSpace, PhysicalSpace, VirtualSpace, TrainingSpaceResource


# Inline Classes
# -------------------------------------------------------
class TrainingSpaceResourceInlineAdmin(admin.StackedInline):
    model = TrainingSpaceResource
    extra = 0
    fields = ['type', 'extra_data']

    formfield_overrides = {pgfields.JSONField: {"widget": JSONEditor}}


# Admin classes
# -------------------------------------------------------
class PhysicalSpaceAdmin(CustomBaseAdmin):
    list_display = ['id', 'name', 'type', 'location']
    list_display_links = ['id', 'name']

    inlines = [TrainingSpaceResourceInlineAdmin]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = (('', '---------'),) + TrainingSpace.Type.PHYSICAL_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class VirtualSpaceAdmin(CustomBaseAdmin):
    list_display = ['id', 'name', 'type']
    list_display_links = ['id', 'name']

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = TrainingSpace.Type.VIRTUAL_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(PhysicalSpace, PhysicalSpaceAdmin)
admin.site.register(VirtualSpace, VirtualSpaceAdmin)
