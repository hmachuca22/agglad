# -*- coding: utf-8 -*-
from django.urls import include, path

from . import views

app_name = 'core'

training_calls_patterns = (
    [
        path(
            "",
            view=views.TrainingCallDashboardView.as_view(),
            name="dashboard"
        ),
        path(
            "all/",
            view=views.TrainingCallListView.as_view(),
            name="training-calls"
        ),
        path(
            "<slug:training_call_slug>/",
            view=views.TrainingCallDetailView.as_view(),
            name="training-call-detail"
        ),
        path(
            "simple-training-call/add/",
            view=views.SimpleTrainingCallCUView.as_view(),
            kwargs=dict(action=views.TrainingCallCUMixin.Action.CREATE),
            name="add-simple-training-call"
        ),
        path(
            "simple-training-call/<slug:training_call_slug>/update/",
            view=views.SimpleTrainingCallCUView.as_view(),
            kwargs=dict(action=views.TrainingCallCUMixin.Action.UPDATE),
            name="update-simple-training-call"
        ),
        path(
            "composite-training-call/add/",
            view=views.CompositeTrainingCallCUView.as_view(),
            kwargs=dict(action=views.TrainingCallCUMixin.Action.CREATE),
            name="add-composite-training-call"
        ),
        path(
            "composite-training-call/<slug:training_call_slug>/update/",
            view=views.CompositeTrainingCallCUView.as_view(),
            kwargs=dict(action=views.TrainingCallCUMixin.Action.UPDATE),
            name="update-composite-training-call"
        ),
        path(
            "<slug:training_call_slug>/groups/",
            view=views.TrainingCallGroupsView.as_view(),
            name="training-call-groups"
        ),
        path(
            "<slug:training_call_slug>/training-unit/<slug:training_unit_slug>/add/",
            view=views.TrainingCallCUGroupView.as_view(),
            kwargs=dict(action=views.TrainingCallCUGroupView.Action.CREATE),
            name="add-training-call-group"
        ),
        path(
            "<slug:training_call_slug>/training-unit/<slug:training_unit_slug>/groups/<int:group_pk>/update/",
            view=views.TrainingCallCUGroupView.as_view(),
            kwargs=dict(action=views.TrainingCallCUGroupView.Action.UPDATE),
            name="update-training-call-group"
        ),
    ],
    "training-calls"
)

urlpatterns = [
    path(
        'contact/',
        view=views.ContactView.as_view(),
        name='contact'
    ),
    path(
        'dashboard/',
        view=views.DashboardView.as_view(),
        name='dashboard'
    ),

    path("training-calls/", include(training_calls_patterns)),

    # Estadísticas y reportes
    path(
        'reports/stats/',
        view=views.PrivateStatsView.as_view(),
        name='stats'
    ),
    
    path(
        'reports/deserters/',
        view=views.DesertersListView.as_view(),
        name='deserters'
    ),

    path(
        'reports/employee-types/',
        view=views.EmployeeTypesView.as_view(),
        name='employee-types'
    ),

    path(
        'reports/participants/',
        view=views.ParticipantsView.as_view(),
        name='participants'
    ),
    
    path(
        'reports/participants/export/',
        view=views.ParticipantsExportView.as_view(),
        name='participants-export'
    ),
    
    # Public links
    path(
        'list-public-links/',
        view=views.PublicLinksListView.as_view(),
        name='list-public-links'
    ),

    path(
        'add-public-links/',
        view=views.PublicLinksCreateView.as_view(),
        name='add-public-links'
    ),

    path(
        'public-links/<int:pk>/update/',
        view=views.PublicLinksUpdateView.as_view(),
        name='public-links-update'
    ),

    path(
        'public-links/<int:pk>/delete/',
        view=views.PublicLinksDeleteView.as_view(),
        name='public-links-delete'
    ),
    
    # Team
    path(
        'team/',
        view=views.TeamListView.as_view(),
        name='team'
    ),

    path(
        'team/add/',
        view=views.TeamCreateView.as_view(),
        name='team-add'
    ),

    path(
        'team/<int:pk>/update/',
        view=views.TeamUpdateView.as_view(),
        name='team-update'
    ),

    path(
        'team/<int:pk>/delete/',
        view=views.TeamDeleteView.as_view(),
        name='team-delete'
    ),
]
