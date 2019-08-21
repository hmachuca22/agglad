# -*- coding: utf-8 -*-
from django.urls import include, path
from . import views

app_name = "spaces"

physical_spaces_patterns = (
    [
        path(
            "",
            view=views.PhysicalSpacesDashboardView.as_view(),
            name="dashboard"
        ),
        path(
            "all/",
            view=views.PhysicalSpacesListView.as_view(),
            name="all"
        ),
        path(
            "add/",
            view=views.PhysicalSpaceCUFormView.as_view(),
            name="add",
            kwargs={"action": views.PhysicalSpaceCUFormView.Action.CREATE}
        ),
        path(
            "<int:pk>/update/",
            view=views.PhysicalSpaceCUFormView.as_view(),
            name="update",
            kwargs={"action": views.PhysicalSpaceCUFormView.Action.UPDATE}
        ),
        path(
            "<int:pk>/delete/",
            view=views.TrainingSpaceDeleteView.as_view(),
            name="delete"
        ),
    ],
    "physical-spaces"
)

urlpatterns = [
    path("physical-spaces/", include(physical_spaces_patterns)),
]
