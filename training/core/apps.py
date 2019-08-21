# -*- coding: utf-8 -*-
from functools import partial

from django.apps import AppConfig
from django.db.models.signals import post_save

from training.utils.signals import set_unique_slug, set_slug
from .signals import copy_tag_to_ancestor


class CoreAppConfig(AppConfig):
    name = "training.core"
    verbose_name = "Core"

    def ready(self):
        post_save.connect(receiver=set_unique_slug, sender='core.TrainingUnit')
        post_save.connect(receiver=set_unique_slug, sender='core.Training')
        post_save.connect(receiver=set_unique_slug, sender='core.Diplomat')
        post_save.connect(receiver=set_unique_slug, sender='core.Seminar')
        post_save.connect(receiver=set_unique_slug, sender='core.Workshop')
        post_save.connect(receiver=set_unique_slug, sender='core.Course')
        post_save.connect(receiver=set_unique_slug, sender='core.Module')
        post_save.connect(receiver=partial(set_slug, base_field='display_name'), sender='core.Tag', weak=False)
        post_save.connect(receiver=copy_tag_to_ancestor, sender='core.TrainingUnitTag')
