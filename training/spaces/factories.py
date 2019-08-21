# -*- coding: utf-8 -*-
import factory

from . import models


class TrainingSpaceFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Space {num}')
    description = 'Description'

    class Meta:
        model = models.TrainingSpace


class PhysicalSpaceFactory(TrainingSpaceFactory):
    class Meta:
        model = models.PhysicalSpace


class VirtualSpaceFactory(TrainingSpaceFactory):
    class Meta:
        model = models.VirtualSpace


class AuditoriumFactory(PhysicalSpaceFactory):
    name = factory.sequence(lambda num: f'Auditorium {num}')
    type = models.TrainingSpace.Type.AUDITORIUM


class ComputerLabFactory(PhysicalSpaceFactory):
    name = factory.sequence(lambda num: f'Computer Lab {num}')
    type = models.TrainingSpace.Type.COMPUTER_LAB


class WebPortalFactory(VirtualSpaceFactory):
    name = factory.sequence(lambda num: f'Web portal {num}')
    type = models.TrainingSpace.Type.WEB_PORTAL


class TrainingSpaceResourceFactory(factory.django.DjangoModelFactory):
    training_space = factory.SubFactory(PhysicalSpaceFactory)

    class Meta:
        model = models.TrainingSpaceResource
