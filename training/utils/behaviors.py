# -*- coding: utf-8 -*-
from django.db import models


class TimeStampedModel(models.Model):
    # Fields
    # -------------------------------------------------------
    created_by = models.CharField('Creado por', max_length=30, default='system')
    created_at = models.DateTimeField('Creado el', auto_now_add=True)
    updated_by = models.CharField('Última modificación por', max_length=30, default='')
    updated_at = models.DateTimeField('Última modificación el', auto_now=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        abstract = True
