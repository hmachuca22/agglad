# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.postgres import fields as pgfields

from jsoneditor.forms import JSONEditor

from training.utils.admin import CustomBaseAdmin
from .models import Group, Enrollment, ClassRoom


class GroupAdmin(CustomBaseAdmin):
    fields = [
        'name', 'training_call', 'training_unit', 'modality', 'teacher', 'quotas', 'classes_starts_at',
        'classes_ends_at', 'settings'
    ]
    list_display = ['id', 'name', 'modality', 'teacher', 'classes_starts_at']
    list_display_links = ['id', 'name']

    formfield_overrides = {pgfields.JSONField: {"widget": JSONEditor}}


class EnrollmentAdmin(CustomBaseAdmin):
    list_display = ['id', 'group', 'student', 'status']
    list_display_links = ['id', 'student']


class ClassRoomAdmin(CustomBaseAdmin):
    list_display = ['id', 'group', 'space']
    list_display_links = ['id', 'group']


admin.site.register(Group, GroupAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
