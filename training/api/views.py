# -*- coding: utf-8 -*-
from django.db.models import Case, When, Value, IntegerField, Q

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from training.core.models import TrainingUnitTag, TrainingCall
from training.organizations.models import Organization
from training.enrollment.models import Enrollment, Group
from training.users.models import User

from .serializers import (
    AreaListSerializer, TrainingCallListSerializer, OrganizationListSerializer, TrainingPlanListSerializer,
    UserListSerializer, EnrollmentUpdateSerializer, EnrollmentDestroySerializer, GroupDestroySerializer,
    OrganizationDestroySerializer
)
from .generics import CustomListAPIView


class AreaListAPIView(ListAPIView):
    serializer_class = AreaListSerializer

    def filter_queryset(self, queryset):
        queryset = super(AreaListAPIView, self).filter_queryset(queryset)

        filters = {}
        if self.kwargs['resource_name'] == 'counties':
            filters['parent__code'] = self.kwargs.get('state_code')
            filters['parent__parent__code'] = self.kwargs.get('country_code')
        elif self.kwargs['resource_name'] == 'states':
            filters['parent__code'] = self.kwargs.get('country_code')

        return queryset.filter(**filters).order_by('code')


class TrainingSpaceListAPIView(CustomListAPIView):
    def filter_queryset(self, queryset):
        queryset = super(TrainingSpaceListAPIView, self).filter_queryset(queryset)

        if self.kwargs['resource_name'] == 'physical-spaces':
            serializer = self.get_serializer(data=self.request.query_params)
            if serializer.is_valid(raise_exception=True):
                filters = dict()
                for field in ['type', 'organization', 'location']:
                    value = serializer.validated_data.get(field)
                    if value:
                        filters[f'{field}__in'] = value

                return queryset.filter(**filters).order_by('name')

        return queryset


class OrganizationListAPIView(CustomListAPIView):
    serializer_class = OrganizationListSerializer
    queryset = Organization.objects.all()

    def filter_queryset(self, queryset):
        queryset = super(OrganizationListAPIView, self).filter_queryset(queryset)

        serializer = self.get_serializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            filters = dict()

            types = serializer.validated_data.get('type')
            if types:
                filters['type__in'] = types

            locations = serializer.validated_data.get('location')
            if locations:
                filters['jurisdiction__in'] = locations

            return queryset.filter(**filters).order_by('type', 'code')


class TrainingCallListAPIView(ListAPIView):
    serializer_class = TrainingCallListSerializer
    limit = None
    permission_classes = []

    def filter_queryset(self, queryset):
        queryset = super(TrainingCallListAPIView, self).filter_queryset(queryset)

        serializer = self.get_serializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            filters = dict()

            statuses = serializer.validated_data.get('status')
            if statuses:
                filters['status__in'] = statuses

            tags = serializer.validated_data.get('tag')
            if tags:
                training_plans = TrainingUnitTag.objects.filter(
                    training_unit__parent=None, tag__slug__in=tags
                ).values_list(
                    'training_unit', flat=True
                )

                filters['training_plan__in'] = training_plans

            # Se ordena el queryset para que siempre aparezcan primero las capacitaciones programados y en curso, sin
            # importar la fecha de comienzo de estas.
            queryset = queryset.filter(
                **filters
            ).annotate(
                priority=Case(
                    When(status=TrainingCall.Status.PUBLISHED, then=Value(1)),
                    When(status=TrainingCall.Status.IN_PROGRESS, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField()
                )
            ).order_by('priority', '-start_date', 'pk')

            if isinstance(self.limit, int):
                return queryset[:self.limit]

            return queryset


class TrainingPlanListAPIView(ListAPIView):
    serializer_class = TrainingPlanListSerializer

    def filter_queryset(self, queryset):
        queryset = super(TrainingPlanListAPIView, self).filter_queryset(queryset)

        serializer = self.get_serializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            filters = dict()

            for field in ['status', 'type']:
                value = serializer.validated_data.get(field)
                if value:
                    filters[f'{field}__in'] = value

            name = serializer.validated_data.get('name')
            if name:
                filters['name__icontains'] = name

            return queryset.filter(**filters).order_by('name')


class UserListAPIView(CustomListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.exclude(is_superuser=True)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        serializer = self.get_serializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            kwargs_filters = dict()
            args_filters = []

            roles = serializer.validated_data.get('role')
            if roles:
                for role in roles:
                    kwargs_filters[f"is_{role}"] = True

            genders = serializer.validated_data.get("gender")
            if genders:
                kwargs_filters["gender__in"] = genders

            name = serializer.validated_data.get("name")
            username = serializer.validated_data.get("username")

            if name and username:
                args_filters.append(Q(full_name__icontains=name) | Q(username__icontains=username))
            else:
                if name:
                    kwargs_filters["full_name__icontains"] = name
                elif username:
                    kwargs_filters["username__icontains"] = username

            return queryset.filter(*args_filters, **kwargs_filters).order_by("username", "pk")


class EnrollmentUpdateAPIView(UpdateAPIView):
    serializer_class = EnrollmentUpdateSerializer
    queryset = Enrollment.objects.all()


class EnrollmentDestroyAPIView(DestroyAPIView):
    serializer_class = EnrollmentDestroySerializer
    queryset = Enrollment.objects.all()


class GroupDestroyAPIView(DestroyAPIView):
    serializer_class = GroupDestroySerializer
    queryset = Group.objects.all()


class OrganizationDestroyAPIView(DestroyAPIView):
    serializer_class = OrganizationDestroySerializer
    queryset = Organization.objects.all()

