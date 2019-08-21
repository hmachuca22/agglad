# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView
from django.views import defaults as default_views
from . import views

app_name = 'enrollment'

urlpatterns = [
    # GROUPS
    path(
        'group/',
        view=views.GroupListView.as_view(),
        name='group-list'
    ),
    path(
        'group/<int:pk>/add/',
        view=views.GroupAddView.as_view(),
        name='group-add'
    ),
    path(
        'group/<int:pk>/update/',
        view=views.GroupUpdateView.as_view(),
        name='group-update'
    ),   
    # CLASS ROOMS
    # path(
    #     'class-room/',
    #     view=views.ClassRoomListView.as_view(),
    #     name='class-room-list'
    # ),
    # path(
    #     'class-room/add/',
    #     view=views.ClassRoomAddView.as_view(),
    #     name='class-room-add'
    # ),


    # ENROLLMENT
    path(
        'enrollment/<int:pk>/list/',
        views.EnrollmentListView.as_view(),
        name='enrollment'
    ),
    path(
        'enrollment/add/',
        view=views.EnrollmentAddView.as_view(),
        name='enrollment-add'
    ),
    path(
        'enrollment/<int:pk>/print/',
        view=views.EnrollmentPrintView.as_view(),
        name='enrollment-print'
    ),
    path(
        'enrollment/<int:pk>/participation-print/',
        view=views.EnrollmentParticipationPrintView.as_view(),
        name='enrollment-participation-print'
    ),
    path(
        'enrollment/<int:student>/history-print/',
        view=views.EnrollmentHistoryPrintView.as_view(),
        name='enrollment-history'
    ),
    path(
        'enrollment/certification-print/<slug:uuid>/',
        view=views.EnrollmentCertificationPrintView.as_view(),
        name='enrollment-certificate-print'
    ),
]
