# -*- coding: utf-8 -*-
import factory

from . import models


class OrganizationFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Organization {num}')
    code = factory.sequence(lambda num: str(num).zfill(6))

    class Meta:
        model = models.Organization


class RegionalCenterFactory(OrganizationFactory):
    name = factory.sequence(lambda num: f'Regional center {num}')
    type = models.Organization.Type.REGIONAL_CENTER


class NGOFactory(OrganizationFactory):
    name = factory.sequence(lambda num: f'NGO {num}')
    type = models.Organization.Type.NGO


class DepartmentalFactory(OrganizationFactory):
    name = factory.sequence(lambda num: f'Departmental {num}')
    type = models.Organization.Type.DEPARTMENTAL


class DistrictFactory(OrganizationFactory):
    name = factory.sequence(lambda num: f'District {num}')
    type = models.Organization.Type.DISTRICT


class OrganizationAreaFactory(factory.django.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)
    area = factory.SubFactory('core.factories.AreaFactory')

    class Meta:
        model = models.OrganizationArea
