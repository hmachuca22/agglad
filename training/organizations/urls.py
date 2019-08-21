# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = 'organizations'

urlpatterns = [
    path(
        "",
        view=views.OrganizationDashboardView.as_view(),
        name="dashboard"
    ),
    path(
        'all/',
        view=views.OrganizationListView.as_view(),
        name='organizations'
    ),
    path(
        'add/',
        view=views.OrganizationCreateView.as_view(),
        name='organization-add'
    ),
    path(
        '<int:pk>/update/',
        view=views.OrganizationUpdateView.as_view(),
        name='organization-update'
    ),
    path(
        '<int:pk>/delete/',
        view=views.OrganizationDeleteView.as_view(),
        name='organization-delete'
    ),

    # Manage organizational users
    path(
        '<int:pk>/users/',
        view=views.OrganizationUsersListView.as_view(),
        name='organization-user-list'
    ),
    path("<int:pk>/users/add/", view=views.OrganizationUserCreateView.as_view(), name="add-organization-user"),
    path(
        'organization/<int:pk>/user/add/',
        view=views.OrganizationUserTemplateView.as_view(),
        name='organization-user-add'
    ),
    path(
        'organization/<int:pk>/user/<int:userpk>/inactivate/',
        view=views.OrganizationUserInactivateView.as_view(),
        name='organization-user-inactivate'
    ),
    path(
        'organization/<int:pk>/user/<int:userpk>/activate/',
        view=views.OrganizationUserActivateView.as_view(),
        name='organization-user-activate'
    ),
]
