# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import (
    DateField, CharField, ModelForm, BaseModelFormSet, modelformset_factory, ChoiceField, ModelChoiceField,
    RadioSelect, HiddenInput, IntegerField
)

from training.core.models import Resource, AvatarResource
from training.organizations.models import UserOrganization
from .models import UserAcademicDegree, UserExternalTraining

User = get_user_model()


# Admin Forms
# -------------------------------------------------------
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    birth_day = DateField(input_formats=('%d/%m/%Y','%Y-%m-%d',),)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return True

        return False


# Views Forms
# -------------------------------------------------------
class UserForm(ModelForm):
    avatar = ModelChoiceField(widget=RadioSelect, queryset=AvatarResource.objects.all().order_by("extra_data__gender"))
    password = CharField(required=False,widget=forms.PasswordInput())
    organization = IntegerField(widget=HiddenInput, required=False)
    current_position_name = CharField(required=False)
    current_position_start_date = DateField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.id:
            self.fields["current_position_name"].initial = instance.current_position_name
            self.fields["current_position_start_date"].initial = instance.current_position_start_date
            if instance.is_organizational:
                user_organization = UserOrganization.objects.filter(user=instance).first()
                if user_organization:
                    self.fields["organization"].initial = user_organization.organization.pk

    class Meta:
        model = User
        fields = [
            "avatar",
            "username",
            "first_name",
            "last_name",
            "email",
            "alternative_email",
            "phone_number",
            "alternative_phone_number",
            "gender",
            "birth_day",
            "residence_place",
            "is_student",
            "is_teacher",
            "is_organizational",
            "organization",
            "employee_type",
            "current_position_name",
            "current_position_start_date"
        ]

    def save(self, commit=True):
        current_position = self.instance.current_position
        if self.cleaned_data["current_position_name"]:
            current_position[User.ExtraDataKeys.CurrentPosition.NAME] = self.cleaned_data["current_position_name"]

        if self.cleaned_data["current_position_start_date"]:
            current_position[
                User.ExtraDataKeys.CurrentPosition.START_DATE
            ] = str(self.cleaned_data["current_position_start_date"])

        self.instance.extra_data[User.ExtraDataKeys.CURRENT_POSITION] = current_position

        return super().save(commit=commit)


class UserAcademicDegreeForm(ModelForm):
    class Meta:
        model = UserAcademicDegree
        fields = ["type", "achieved_title", "study_center", "started_at", "finished_at"]


class UserExternalTrainingForm(ModelForm):
    class Meta:
        model = UserExternalTraining
        fields = [
            "type", "name", "description", "location", "started_at", "finished_at", "duration", "modality", "tags"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].required = False


# FormSet Factories
# -------------------------------------------------------
UserAcademicDegreeFormSetFactory = modelformset_factory(
    UserAcademicDegree, form=UserAcademicDegreeForm, extra=1, min_num=0, validate_min=True, can_delete=True
)
UserExternalTrainingFormSetFactory = modelformset_factory(
    UserExternalTraining, form=UserExternalTrainingForm, extra=1, min_num=0, validate_min=True, can_delete=True
)


# FormSets
# -------------------------------------------------------
class UserAcademicDegreeFormSet(UserAcademicDegreeFormSetFactory):
    pass


class UserExternalTrainingFormSet(UserExternalTrainingFormSetFactory):
    pass


class UserUpdateForm(ModelForm):
    birth_day = DateField(input_formats=('%d/%m/%Y','%Y-%m-%d',),)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'birth_day',
            'is_student',
            'is_teacher',
        ]
