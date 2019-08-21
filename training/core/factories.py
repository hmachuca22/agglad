# -*- coding: utf-8 -*-
import datetime
import factory

from django.utils import timezone

from training.organizations import factories as organizations_factories
from . import models


class AreaFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Area {num}')
    code = factory.sequence(lambda num: f'C{num}')

    class Meta:
        model = models.Area


class CountryFactory(AreaFactory):
    name = factory.sequence(lambda num: f'Country {num}')
    type = models.Area.Type.COUNTRY
    parent = None


class StateFactory(AreaFactory):
    name = factory.sequence(lambda num: f'State {num}')
    type = models.Area.Type.STATE
    parent = factory.SubFactory(CountryFactory)


class CountyFactory(AreaFactory):
    name = factory.sequence(lambda num: f'County {num}')
    type = models.Area.Type.COUNTY
    parent = factory.SubFactory(StateFactory)


class TagFactory(factory.django.DjangoModelFactory):
    display_name = factory.sequence(lambda num: f'Tag {num}')

    class Meta:
        model = models.Tag


class TrainingUnitFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Training {num}')
    description = factory.sequence(lambda num: f'Description {num}')
    content = factory.sequence(lambda num: f'Content {num}')
    order = factory.sequence(lambda num: num)
    duration = 120

    class Meta:
        model = models.TrainingUnit


class TrainingFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Training {num}')
    type = models.TrainingUnit.Type.TRAINING


class DiplomatFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Diplomat {num}')
    type = models.TrainingUnit.Type.DIPLOMAT


class CourseFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Course {num}')
    type = models.TrainingUnit.Type.COURSE


class WorkshopFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Workshop {num}')
    type = models.TrainingUnit.Type.WORKSHOP


class SeminarFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Seminar {num}')
    type = models.TrainingUnit.Type.SEMINAR


class ModuleFactory(TrainingUnitFactory):
    name = factory.sequence(lambda num: f'Module {num}')
    type = models.TrainingUnit.Type.MODULE


class TrainingUnitTagFactory(factory.django.DjangoModelFactory):
    training_unit = factory.SubFactory(TrainingUnitFactory)
    tag = factory.SubFactory(TagFactory)

    class Meta:
        model = models.TrainingUnitTag


class TrainingCallFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Training Call {num}')
    training_plan = factory.SubFactory(TrainingUnitFactory)
    owner = factory.SubFactory(organizations_factories.OrganizationFactory)

    class Meta:
        model = models.TrainingCall


class ScheduledTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.SCHEDULED
    start_date = timezone.now() + datetime.timedelta(days=1)
    end_date = timezone.now() + datetime.timedelta(days=2)


class InProgressTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.IN_PROGRESS
    start_date = timezone.now() - datetime.timedelta(days=1)
    end_date = timezone.now() + datetime.timedelta(days=1)


class CancelledTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.CANCELLED


class SuspendedTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.SUSPENDED


class PostponedTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.POSTPONED


class FinishedTrainingCallFactory(TrainingCallFactory):
    status = models.TrainingCall.Status.FINISHED
    start_date = timezone.now() - datetime.timedelta(days=2)
    end_date = timezone.now() - datetime.timedelta(days=1)


class SponsorFactory(factory.django.DjangoModelFactory):
    training_call = factory.SubFactory(TrainingCallFactory)
    organization = factory.SubFactory(organizations_factories.OrganizationFactory)

    class Meta:
        model = models.Sponsor
