# -*- coding: utf-8 -*-
from django.db import models

from . import models as spaces_models


class VirtualSpaceManager(models.Manager):
    def get_queryset(self):
        return super(VirtualSpaceManager, self).get_queryset().filter(
            type__in=spaces_models.TrainingSpace.Type.VIRTUAL_TYPES
        )


class PhysicalSpaceManager(models.Manager):
    def get_queryset(self):
        return super(PhysicalSpaceManager, self).get_queryset().filter(
            type__in=spaces_models.TrainingSpace.Type.PHYSICAL_TYPES
        )
