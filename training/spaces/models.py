# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres import fields as pg_fields
from django.urls import reverse

from training.core.models import Area
from training.organizations.models import Organization
from training.spaces.managers import VirtualSpaceManager, PhysicalSpaceManager


class TrainingSpace(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:
        # TODO: Estandarizar tipos de espacios
        AUDITORIUM = 'auditorium'
        CLASS_ROOM = 'class_room'
        COMPUTER_LAB = 'computer_lab'
        WEB_PORTAL = 'web_portal'

        PHYSICAL_TYPES = [AUDITORIUM, COMPUTER_LAB, CLASS_ROOM]
        PHYSICAL_CHOICES = (
            (AUDITORIUM, 'Auditorio'),
            (COMPUTER_LAB, 'Laboratorio de computación'),
            (CLASS_ROOM, 'Aula')
        )

        VIRTUAL_TYPES = [WEB_PORTAL]
        VIRTUAL_CHOICES = (
            (WEB_PORTAL, 'Portal web'),
        )

        CHOICES = PHYSICAL_CHOICES + VIRTUAL_CHOICES

    class SettingsKeys:
        WEBSITE_URL = 'website_url'
        DRIVER = 'driver'
        CONTACTS = 'contacts'

        class DriverKeys:
            PATH = 'path'
            CREDENTIALS = 'credentials'

    # Fields
    # -------------------------------------------------------
    name = models.CharField('Nombre', max_length=50)
    description = models.CharField('Descripción', max_length=300)
    type = models.CharField('Tipo', max_length=30, choices=Type.CHOICES)
    location = models.ForeignKey(
        Area, on_delete=models.CASCADE, verbose_name='Localización', null=True, blank=True, related_name='area_space'
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name='Organización', null=True, blank=True
    )
    """
    Examples:
        settings: {
            'website_url': 'https://websitespace.io/',
            'driver': {  # En caso de ser un espacio virtual
                'path': 'path.to.virtual.space.driver',
                'credentials': {
                    'username': 'username',
                    'password': 'password'
                }
            },
            'contacts' : [
                {'name': 'John Doe', 'email': 'john@doe.com'},
                {'name': 'Jane Doe', 'email': 'jane@doe.com', 'phone': '+50499999999'}
            ]
        }
    """
    settings = pg_fields.JSONField('Configuraciones', default=dict, blank=True, null=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'training_space'
        verbose_name = 'Espacio de formación'
        verbose_name_plural = 'Espacios de formación'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.name

    # Properties
    # -------------------------------------------------------
    @property
    def website_url(self):
        return self.settings.get(self.SettingsKeys.WEBSITE_URL, '')

    @property
    def driver_settings(self):
        return self.settings.get(self.SettingsKeys.DRIVER, {})

    @property
    def driver_path(self):
        return self.driver_settings.get(self.SettingsKeys.DriverKeys.PATH, '')

    @property
    def contacts(self):
        return self.settings.get(self.SettingsKeys.CONTACTS, [])

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            type=self.type,
            type_label=self.get_type_display()
        )

    def get_absolute_url(self):
        return reverse("spaces:space-update", kwargs={"pk": self.pk})


class VirtualSpace(TrainingSpace):
    # Managers
    # -------------------------------------------------------
    objects = VirtualSpaceManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Espacio virtual'
        verbose_name_plural = 'Espacios virtuales'


class PhysicalSpace(TrainingSpace):
    # Managers
    # -------------------------------------------------------
    objects = PhysicalSpaceManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Espacio físico'
        verbose_name_plural = 'Espacios físicos'

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        representation = super(PhysicalSpace, self).to_representation()
        representation['resources'] = [resource.to_representation() for resource in self.trainingspaceresource_set.all()]
        representation['location'] = self.location.to_representation()

        return representation


class TrainingSpaceResource(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:  # TODO: Ampliar lista de recursos
        TV = 'tv'
        VIDEO_PROJECTOR = 'video_projector'
        DESKTOP_COMPUTER = 'desktop_computer'
        LAPTOP = 'laptop'
        WIFI = 'wifi'

        CHOICES = (
            (TV, 'Televisor'),
            (VIDEO_PROJECTOR, 'Video proyector'),
            (DESKTOP_COMPUTER, 'Computadora de escritorio'),
            (LAPTOP, 'Computadora portatil'),
            (WIFI, 'Wifi')
        )

    class ExtraDataKeys:
        QUANTITY = 'quantity'
        DESCRIPTION = 'description'

        class TVType:
            QUANTITY = 'quantity'
            DESCRIPTION = 'description'

            SKELETON = {

            }

    # Fields
    # -------------------------------------------------------
    type = models.CharField('Tipo', max_length=30, choices=Type.CHOICES)
    training_space = models.ForeignKey(TrainingSpace, on_delete=models.CASCADE, verbose_name='Espacio de formación')
    """
    Examples:
        extra_data = {
            'quantity': 4,
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'training_space_resource'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.get_type_display()

    def to_representation(self):
        return dict(
            id=self.id,
            type=self.type,
            type_label=self.get_type_display()
        )
