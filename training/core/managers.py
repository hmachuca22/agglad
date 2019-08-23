# -*- coding: utf-8 -*-
from django.db import models

from . import models as core_models

class CountryManager(models.Manager):
    def get_queryset(self):
        return super(CountryManager, self).get_queryset().filter(type=core_models.Area.Type.COUNTRY)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.Area.Type.COUNTRY})
        return super(CountryManager, self).create(**kwargs)


class StateManager(models.Manager):
    def get_queryset(self):
        return super(StateManager, self).get_queryset().filter(type=core_models.Area.Type.STATE)

    def create(self, **kwargs):
        print('Actualizando')
        kwargs.update({'type': core_models.Area.Type.STATE})
        return super(StateManager, self).create(**kwargs)


class CountyManager(models.Manager):
    def get_queryset(self):
        return super(CountyManager, self).get_queryset().filter(type=core_models.Area.Type.COUNTY)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.Area.Type.COUNTY})
        return super(CountyManager, self).create(**kwargs)


class VillageManager(models.Manager):
    def get_queryset(self):
        return super(VillageManager, self).get_queryset().filter(type=core_models.Area.Type.VILLAGE)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.Area.Type.VILLAGE})
        return super(VillageManager, self).create(**kwargs)


class TrainingManager(models.Manager):
    def get_queryset(self):
        return super(TrainingManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.TRAINING)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.TRAINING})
        return super(TrainingManager, self).create(**kwargs)


class DiplomatManager(models.Manager):
    def get_queryset(self):
        return super(DiplomatManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.DIPLOMAT)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.DIPLOMAT})
        return super(DiplomatManager, self).create(**kwargs)


class CourseManager(models.Manager):
    def get_queryset(self):
        return super(CourseManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.COURSE)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.COURSE})
        return super(CourseManager, self).create(**kwargs)


class WorkshopManager(models.Manager):
    def get_queryset(self):
        return super(WorkshopManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.WORKSHOP)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.WORKSHOP})
        return super(WorkshopManager, self).create(**kwargs)


class SeminarManager(models.Manager):
    def get_queryset(self):
        return super(SeminarManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.SEMINAR)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.SEMINAR})
        return super(SeminarManager, self).create(**kwargs)


class ModuleManager(models.Manager):
    def get_queryset(self):
        return super(ModuleManager, self).get_queryset().filter(type=core_models.TrainingUnit.Type.MODULE)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.TrainingUnit.Type.MODULE})
        return super(ModuleManager, self).create(**kwargs)


class AvatarResourceManager(models.Manager):
    def get_queryset(self):
        return super(AvatarResourceManager, self).get_queryset().filter(type=core_models.Resource.Type.AVATAR)

    def create(self, **kwargs):
        kwargs.update({'type': core_models.Resource.Type.AVATAR})
        return super(AvatarResourceManager, self).create(**kwargs)
