# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.postgres import fields as pgfields
from django.utils.html import format_html

from jsoneditor.forms import JSONEditor

from training.utils.admin import CustomBaseAdmin
from .forms import CustomUserChangeForm,  CustomUserCreationForm
from .models import OrganizationalProfile, UserAcademicDegree, UserExternalTraining, UserEmployeeType

User = get_user_model()


# Admin Classes
# -------------------------------------------------------
@admin.register(User)
class CustomUserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("ROLES", {"fields": ("is_student", "is_teacher", "is_organizational", "is_admin")}),
        ("EXTRA FIELDS", {"fields": ("birth_day", "extra_data")}),
    )
    list_display = ["username", "full_name", "birth_day", "avatar_preview", "is_active"]
    search_fields = ["username"]

    formfield_overrides = {pgfields.JSONField: {"widget": JSONEditor}}

    def avatar_preview(self, obj):
        print('Objeto---------------------___>', obj,'<<<<-------------------------')
        if obj is None:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="75" /></a>',
                obj.avatar.asset.url,
                obj.avatar.asset.url
            )
        else:
            return 'No disponible'
    avatar_preview.short_description = "Avatar"


class UserAcademicDegreeAdmin(CustomBaseAdmin):
    fields = ["user", "type", "achieved_title", "study_center", "started_at", "finished_at"]
    list_display = ["id", "user", "type", "achieved_title"]
    list_display_links = ["id", "user", "type", "achieved_title"]


class UserExternalTrainingAdmin(CustomBaseAdmin):
    fields = ["user", "type", "name", "description", "location", "started_at", "finished_at", "modality", "duration", "tags"]
    list_display = ["id", "type", "user", "name", "location"]
    list_display_links = ["id", "type", "user", "name", "location"]


admin.site.register(UserAcademicDegree, UserAcademicDegreeAdmin)
admin.site.register(UserExternalTraining, UserExternalTrainingAdmin)
admin.site.register(OrganizationalProfile)
admin.site.register(UserEmployeeType)
