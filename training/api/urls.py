# -*- coding: utf-8 -*-
from django.urls import path

from training.core.models import Country, State, County, TrainingUnit, TrainingCall
from training.organizations.models import Organization
from training.spaces.models import PhysicalSpace, VirtualSpace
from . import views
from . import serializers
from . import pagination

app_name = 'api'

urlpatterns = [
    path(
        'countries/',
        view=views.AreaListAPIView.as_view(queryset=Country.objects.all()),
        kwargs={'resource_name': 'countries'},
        name='countries'
    ),
    path(
        'countries/<str:country_code>/states/',
        view=views.AreaListAPIView.as_view(queryset=State.objects.all()),
        kwargs={'resource_name': 'states'},
        name='states'
    ),
    path(
        'countries/<str:country_code>/states/<str:state_code>/counties/',
        view=views.AreaListAPIView.as_view(queryset=County.objects.all()),
        kwargs={'resource_name': 'counties'},
        name='counties'
    ),
    path(
        'physical-spaces/',
        view=views.TrainingSpaceListAPIView.as_view(
            queryset=PhysicalSpace.objects.all(), serializer_class=serializers.PhysicalSpaceListSerializer
        ),
        kwargs={'resource_name': 'physical-spaces'},
        name='physical-spaces'
    ),
    path(
        'virtual-spaces/',
        view=views.TrainingSpaceListAPIView.as_view(
            queryset=VirtualSpace.objects.all(), serializer_class=serializers.VirtualSpaceListSerializer
        ),
        kwargs={'resource_name': 'virtual-spaces'},
        name='virtual-spaces'
    ),
    path(
        'organizations/',
        view=views.OrganizationListAPIView.as_view(),
        name='organizations'
    ),
    path(
        'training-calls/',
        view=views.TrainingCallListAPIView.as_view(
            queryset=TrainingCall.objects.all(),
            pagination_class=pagination.CustomPageNumberPagination
        ),
        name='training-calls'
    ),
    path(
        'training-calls/latest/',
        view=views.TrainingCallListAPIView.as_view(
            queryset=TrainingCall.objects.all(),
            limit=6
        ),
        name='latest-training-calls'
    ),
    path(
        'training-plans/',
        view=views.TrainingPlanListAPIView.as_view(
            queryset=TrainingUnit.objects.filter(parent=None),
            pagination_class=pagination.CustomPageNumberPagination
        ),
        name='training-plans'
    ),
    path('users/', view=views.UserListAPIView.as_view(), name='users'),
    path('enrollment/<int:pk>/update/', view=views.EnrollmentUpdateAPIView.as_view(), name='enrollment-update'),
    path('enrollment/<int:pk>/delete/', view=views.EnrollmentDestroyAPIView.as_view(), name='enrollment-delete'),
    path('group/<int:pk>/delete/', view=views.GroupDestroyAPIView.as_view(), name='group-delete'),
    path('organizations/<int:pk>/delete/', view=views.OrganizationDestroyAPIView.as_view(), name='organization-delete'),
]
