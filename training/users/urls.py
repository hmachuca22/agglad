# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(
        "",
        view=views.UserDashboardView.as_view(),
        name="dashboard"
    ),
    path(
        "all/",
        view=views.UserListView.as_view(),
        name="users"
    ),
    path(
        "add/",
        view=views.UserCUFormView.as_view(),
        name="add-user",
        kwargs={"action": views.UserCUFormView.Action.CREATE}
    ),
    path(
        "external-training/template/",
        view=views.UserExternalTrainingTemplate.as_view(),
        name="external-training-template"
    ),
    path(
        "external-training/dump/add",
        view=views.UserExternalTrainingDump.as_view(),
        name="add-external-training-dump"
    ),
    path(
        "external-training/dump/success",
        view=views.UserExternalTrainingSuccess.as_view(),
        name="external-training-success"
    ),
    path(
        "<int:pk>/profile/",
        view=views.UserProfileView.as_view(),
        name="user-profile"
    ),
    path(
        "<int:pk>/update/",
        view=views.UserCUFormView.as_view(),
        name="update-user-profile",
        kwargs={"action": views.UserCUFormView.Action.UPDATE}
    ),
    path(
        "profile",
        view=views.UserProfileView.as_view(),
        name="self-profile"
    ),
    path(
        "profile/update/",
        view=views.UserCUFormView.as_view(),
        name="update-self-profile",
        kwargs={"action": views.UserCUFormView.Action.UPDATE}
    ),
]
