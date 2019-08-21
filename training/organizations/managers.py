# -*- coding: utf-8 -*-
from django.db import models

from . import models as organization_models


class RegionalCenterManager(models.Manager):
    def get_queryset(self):
        return super(RegionalCenterManager, self).get_queryset().filter(
            type=organization_models.Organization.Type.REGIONAL_CENTER
        )

    def create(self, **kwargs):
        kwargs.update({'type': organization_models.Organization.Type.REGIONAL_CENTER})
        return super(RegionalCenterManager, self).create(**kwargs)


class NGOManager(models.Manager):
    def get_queryset(self):
        return super(NGOManager, self).get_queryset().filter(
            type=organization_models.Organization.Type.NGO
        )

    def create(self, **kwargs):
        kwargs.update({'type': organization_models.Organization.Type.NGO})
        return super(NGOManager, self).create(**kwargs)


class DepartmentalManager(models.Manager):
    def get_queryset(self):
        return super(DepartmentalManager, self).get_queryset().filter(
            type=organization_models.Organization.Type.DEPARTMENTAL
        )

    def create(self, **kwargs):
        kwargs.update({'type': organization_models.Organization.Type.DEPARTMENTAL})
        return super(DepartmentalManager, self).create(**kwargs)


class DistrictManager(models.Manager):
    def get_queryset(self):
        return super(DistrictManager, self).get_queryset().filter(
            type=organization_models.Organization.Type.DISTRICT
        )

    def create(self, **kwargs):
        kwargs.update({'type': organization_models.Organization.Type.DISTRICT})
        return super(DistrictManager, self).create(**kwargs)
