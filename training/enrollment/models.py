# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.contrib.postgres import fields as pg_fields

from training.core.models import TrainingUnit, TrainingCall
from training.organizations.models import Organization
from training.spaces.models import TrainingSpace
from training.users.models import User
from training.utils.behaviors import TimeStampedModel


class Group(TimeStampedModel):
    # Constants
    # -------------------------------------------------------
    class Modality:
        FACE_TO_FACE = 'face_to_face'
        VIRTUAL = 'virtual'
        COMBINED = 'combined'

        CHOICES = (
            (FACE_TO_FACE, 'Presencial'),
            (VIRTUAL, 'Virtual'),
            (COMBINED, 'Presencial/Virtual')
        )

    class SettingsKeys:
        ENROLLMENT_RULES = 'enrollment_rules'

    # Fields
    # -------------------------------------------------------
    name = models.CharField('Nombre', max_length=30)
    training_call = models.ForeignKey(TrainingCall, on_delete=models.CASCADE, verbose_name='Convocatoria')
    training_unit = models.ForeignKey(
        TrainingUnit, on_delete=models.CASCADE, verbose_name='Unidad de formación', related_name='training_unit_group'
    )
    modality = models.CharField('Modalidad', max_length=20, choices=Modality.CHOICES)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Facilitador', limit_choices_to={'is_teacher': True}
    )
    quotas = models.PositiveSmallIntegerField('Cupos')
    classes_starts_at = models.DateTimeField('Fecha de inicio de clases', null=True, blank=True)
    classes_ends_at = models.DateTimeField('Fecha de finalización de clases', null=True, blank=True)
    """
    Examples:
        settings = {
            'enrollment_rules': {
                ...
            }
        }
    """
    settings = pg_fields.JSONField('Configuraciones', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'group'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    # Constants
    # -------------------------------------------------------
    class ExtraDataKeys:
        pass

    # Fields
    # -------------------------------------------------------
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Grupo', related_name='group_classroom')
    space = models.ForeignKey(
        TrainingSpace, on_delete=models.CASCADE, verbose_name='Espacio', related_name='space_classroom'
    )
    """
    Examples:
        extra_data = {  # en caso de espacios vituales puede guardarse información del curso (id, token, etc...)
            ...
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'classroom'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.group.name} - {self.space.name}'


class Enrollment(models.Model):
    # Constants
    # -------------------------------------------------------
    class Status:
        RESERVED = 'reserved'
        ACTIVE = 'active'
        CANCELLED = 'canceled'
        APPROVED = 'approved'
        UNAPPROVED = 'unapproved'

        CHOICES = (
            (RESERVED, 'Reservada'),
            (ACTIVE, 'Activa'),
            (CANCELLED, 'Cancelada'),
            (APPROVED, 'Aprobada'),
            (UNAPPROVED, 'No aprobada')
        )

    # Fields
    # -------------------------------------------------------
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Grupo', related_name='group_enrollment')
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Estudiante', limit_choices_to={'is_student': True},
        related_name='user_enrollment'
    )
    status = models.CharField('Estado', max_length=30, choices=Status.CHOICES, db_index=True)
    final_score = models.PositiveSmallIntegerField('Calificación final', default=0)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    """
    Examples:
        extra_data = {
            ...
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'enrollment'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.student.full_name} - {self.group.name}'

    def to_representation(self):
        return dict(
            id=self.id,
            group=self.group.name,
            student=self.student.full_name,
            status=self.status
        )
