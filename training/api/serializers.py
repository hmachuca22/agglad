# -*- coding: utf-8 -*-
from rest_framework import serializers

from training.core.models import Area, TrainingUnit, TrainingCall
from training.organizations.models import Organization
from training.spaces.models import TrainingSpace
from training.users.models import User
from training.enrollment.models import Enrollment


class AreaListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.to_representation()


class PhysicalSpaceListSerializer(serializers.Serializer):
    type = serializers.MultipleChoiceField(choices=TrainingSpace.Type.PHYSICAL_CHOICES)
    organization = serializers.ListField(child=serializers.IntegerField())
    location = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        locations = attrs['location']
        all_locations = []
        for location_id in locations:
            if location_id in all_locations:
                continue

            location = Area.objects.filter(id=location_id).first()
            if location:
                all_locations += location.get_descendants(include_self=True).values_list('id', flat=True)

        attrs['location'] = set(all_locations)

        return attrs

    def to_representation(self, instance):
        return instance.to_representation()


class VirtualSpaceListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.to_representation()


class OrganizationListSerializer(serializers.Serializer):
    type = serializers.MultipleChoiceField(choices=Organization.Type.CHOICES)
    location = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        locations = attrs['location']
        all_locations = []
        for location_id in locations:
            if location_id in all_locations:
                continue

            location = Area.objects.filter(id=location_id).first()
            if location:
                all_locations += location.get_descendants(include_self=True).values_list('id', flat=True)

        attrs['location'] = set(all_locations)

        return attrs

    def to_representation(self, instance):
        return instance.to_representation()


class TrainingCallListSerializer(serializers.Serializer):
    status = serializers.MultipleChoiceField(choices=TrainingCall.Status.CHOICES)
    tag = serializers.ListField(child=serializers.CharField())

    def to_representation(self, instance):
        return instance.to_representation()


class TrainingPlanListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.MultipleChoiceField(choices=TrainingUnit.Type.CHOICES)

    def to_representation(self, instance):
        return instance.to_representation()


class UserListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    role = serializers.MultipleChoiceField(choices=User.Role.CHOICES)
    gender = serializers.MultipleChoiceField(choices=User.Gender.CHOICES)
    status = serializers.MultipleChoiceField(
        choices=(("active", "Usuarios activos"), ("inactive", "Usuarios inactivos"))
    )

    def to_representation(self, instance):
        return instance.to_representation()


class EnrollmentUpdateSerializer(serializers.Serializer):
    status = serializers.MultipleChoiceField(choices=Enrollment.Status.CHOICES)

    def to_representation(self, instance):
        return instance.to_representation()

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        for s in status:
            instance.status = s
        instance.save()
        return instance


class EnrollmentDestroySerializer(serializers.Serializer):
    id = serializers.IntegerField()


class GroupDestroySerializer(serializers.Serializer):
    id = serializers.IntegerField()

class OrganizationDestroySerializer(serializers.Serializer):
    id = serializers.IntegerField()
