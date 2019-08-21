# -*- coding: utf-8 -*-
import factory

from training.core import factories as core_factories
from training.users import factories as users_factories
from . import models


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.sequence(lambda num: f'Group {num}')
    training_call = factory.SubFactory(core_factories.TrainingCallFactory)
    training_unit = factory.SubFactory(core_factories.TrainingUnitFactory)
    teacher = factory.SubFactory(users_factories.TeacherUserFactory)
    quotas = 10

    class Meta:
        model = models.Group
