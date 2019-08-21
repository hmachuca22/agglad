# -*- coding: utf-8 -*-
from django.db import models

from training.utils.behaviors import TimeStampedModel
from .managers import RegionalCenterManager, NGOManager, DepartmentalManager, DistrictManager


class Organization(TimeStampedModel):
    # Constants
    # -------------------------------------------------------
    class Type:
        REGIONAL_CENTER = 'regional_center'
        NGO = 'ngo'
        DEPARTMENTAL = 'departmental'
        DISTRICT = 'district'

        CHOICES = (
            (REGIONAL_CENTER, 'Centro Regional'),
            (NGO, 'ONG'),
            (DEPARTMENTAL, 'Departamental'),
            (DISTRICT, 'Distrital')
        )


    # Fields
    # -------------------------------------------------------
    name = models.CharField('Nombre', max_length=100)
    code = models.CharField('Código', max_length=10)
    type = models.CharField('Tipo', max_length=30, choices=Type.CHOICES)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'organization'
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.name

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        return dict(
            id=self.id,
            name=self.name,
            type=self.type,
            type_label=self.get_type_display(),
            code=self.code
        )


class RegionalCenter(Organization):
    # Managers
    # -------------------------------------------------------
    objects = RegionalCenterManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Centro regional'
        verbose_name_plural = 'Centros regionales'


class NGO(Organization):
    # Managers
    # -------------------------------------------------------
    objects = NGOManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Organización no gubernamental'
        verbose_name_plural = 'Organizaciones no gubernamentales'


class Departmental(Organization):
    # Managers
    # -------------------------------------------------------
    objects = DepartmentalManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Departamental'
        verbose_name_plural = 'Departamentales'


class District(Organization):
    # Managers
    # -------------------------------------------------------
    objects = DistrictManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Distrital'
        verbose_name_plural = 'Distritales'


class UserOrganization(models.Model):
    # Fields
    # -------------------------------------------------------
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name="Usuario", limit_choices_to={"is_organizational": True}
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Organización")

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = "user_organization"
        verbose_name = "Usuario organizacional"
        verbose_name_plural = "Usuarios organizacionales"

