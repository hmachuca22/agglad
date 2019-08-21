# -*- coding: utf-8 -*-
from datetime import date
from operator import itemgetter

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.urls import reverse

from training.core.models import Resource, TrainingUnit
from training.organizations.models import Organization


class UserEmployeeType(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:
        TEACHER = "teacher"
        ADMINISTRATIVE = "administrative"

        ALL = [TEACHER, ADMINISTRATIVE]

        CHOICES = (
            (TEACHER, "Docente"),
            (ADMINISTRATIVE, "Administrativo"),
        )

    # Fields
    # -------------------------------------------------------
    name = models.CharField("Nombre", max_length=150)
    type = models.CharField("Tipo", max_length=30, choices=Type.CHOICES)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'employee_type'
        verbose_name = 'Tipo de Empleado'
        verbose_name_plural = 'Tipos de Empleados'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'


class User(AbstractUser):
    # Constants
    # -------------------------------------------------------
    class Gender:
        MALE = 'male'
        FEMALE = 'female'
        OTHER = 'other'

        ALL = [MALE, FEMALE, OTHER]

        CHOICES = (
            (MALE, 'Masculino'),
            (FEMALE, 'Femenino'),
            (OTHER, 'Otro')
        )

    class Role:
        STUDENT = "student"
        TEACHER = "teacher"
        ORGANIZATIONAL = "organizational"
        ADMIN = "admin"
        SUPERUSER = "superuser"

        ALL = [STUDENT, TEACHER, ORGANIZATIONAL, ADMIN, SUPERUSER]

        CHOICES = (
            (STUDENT, "Estudiante"),
            (TEACHER, 'Facilitador'),
            (ORGANIZATIONAL, 'Usuario organizacional'),
            (ADMIN, 'Administrador'),
            (SUPERUSER, "Super usuario")
        )

    class ExtraDataKeys:
        CURRENT_POSITION = "current_position"

        class CurrentPosition:
            NAME = "name"
            START_DATE = "start_date"

    # Fields
    # -------------------------------------------------------
    first_name = models.CharField('Nombres', max_length=150)
    last_name = models.CharField('Apellidos', max_length=150)
    full_name = models.CharField('Nombre completo', max_length=300, null=True)
    avatar = models.ForeignKey(
        'core.Resource',
        on_delete=models.CASCADE,
        verbose_name='Avatar',
        limit_choices_to={"type": Resource.Type.AVATAR},
        null=True,
        blank=True
    )
    residence_place = models.ForeignKey(
        "core.Area",
        on_delete=models.CASCADE,
        related_name="area_user",
        verbose_name="Lugar de residencia",
        null=True,
        blank=True
    )
    email = models.EmailField('Correo electrónico', blank=True)
    alternative_email = models.EmailField('Correo electrónico alternativo', null=True, blank=True)
    phone_number = models.CharField('Número de teléfono', max_length=15, null=True, blank=True)
    alternative_phone_number = models.CharField('Número de teléfono alternativo', max_length=15, null=True, blank=True)
    gender = models.CharField('Género', choices=Gender.CHOICES, max_length=10)
    birth_day = models.DateField('Fecha de nacimiento', null=True, blank=True)

    employee_type = models.ForeignKey(
        UserEmployeeType, on_delete=models.CASCADE, verbose_name="Tipo de Empleado", null=True, blank=True
    )

    is_student = models.BooleanField('Es estudiante?', default=False)
    is_teacher = models.BooleanField('Es facilitador?', default=False)
    is_organizational = models.BooleanField('Es usuario organizacional?', default=False)
    is_admin = models.BooleanField('Es administrador?', default=False)

    """
    Examples:
        extra_data = {
            'current_position': {
                'name': 'Secretario',
                'start_date': '2018-01-01'
            }
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.full_name

    # Properties
    # -------------------------------------------------------
    @property
    def age(self):
        if self.birth_day:
            today = date.today()
            born = self.birth_day
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return age
        else:
            return 0

    @property
    def age_str(self):
        if self.birth_day:
            today = date.today()
            age = today.year - self.birth_day.year - (
                (today.month, today.day) < (self.birth_day.month, self.birth_day.day))
            return "{} años".format(age, )
        else:
            return " -- "

    @property
    def roles(self):
        role_map = dict(self.Role.CHOICES)

        return [{
            "type": role,
            "type_label": role_map.get(role, "unknown")
        } for role in self.Role.ALL if getattr(self, f"is_{role}", False)]

    @property
    def current_position(self):
        return self.extra_data.get(self.ExtraDataKeys.CURRENT_POSITION, {})

    @property
    def current_position_name(self):
        return self.current_position.get(self.ExtraDataKeys.CurrentPosition.NAME, "")

    @property
    def current_position_start_date(self):
        return self.current_position.get(self.ExtraDataKeys.CurrentPosition.START_DATE, "")

    @property
    def phone_numbers(self):
        return [
            self.phone_number, self.alternative_phone_number
        ] if self.alternative_phone_number else [
            self.phone_number
        ]

    @property
    def emails(self):
        return [self.email, self.alternative_email] if self.alternative_email else [self.email]

    # Methods
    # -------------------------------------------------------
    def save(self, *args, **kwargs):
        full_name = f"{self.first_name} {self.last_name}"
        self.full_name = ' '.join(full_name.split())

        return super().save(*args, **kwargs)

    def get_achievements_record(self):
        """
        Retorna un listado compuesto por las representaciones de los logros académicos del usuario incluyendo tanto
        grados académicos como capacitaciones externas e internas.
        """
        academic_degrees = [degree.to_representation() for degree in UserAcademicDegree.objects.filter(user=self)]
        external_trainings = [training.to_representation() for training in
                              UserExternalTraining.objects.filter(user=self)]
        trainings = []
        for enrollment in self.user_enrollment.filter(status='approved'):
            trainings.append({
                'name': enrollment.group.training_unit.name,
                'type_label': enrollment.group.training_unit.get_type_display(),
                'tags': enrollment.group.training_unit.tags.all().values_list('display_name'),
                'finished_at': enrollment.group.classes_ends_at.date(),
                'location': enrollment.group.group_classroom.all().values_list('space__organization__name')[0][0],
                'uuid': enrollment.uuid
            })

        records = academic_degrees + external_trainings + trainings
        records = sorted(records, key=itemgetter('finished_at'), reverse=True)

        return records

    def get_historic_enroll(self):
        """
        Retorna un listado de capacitaciones actuales e históricas no aprobadas
        """
        trainings = []
        for enrollment in self.user_enrollment.exclude(status='approved'):
            trainings.append({
                'name': enrollment.group.training_unit.name,
                'description': enrollment.group.training_unit.description,
                'type_label': enrollment.group.training_unit.get_type_display(),
                'modality_label': enrollment.group.get_modality_display(),
                'teacher': enrollment.group.teacher.full_name,
                'tags': enrollment.group.training_unit.tags.all().values_list('display_name'),
                'started_at': enrollment.group.classes_starts_at.date(),
                'status_label': enrollment.get_status_display(),
                'duration': enrollment.group.training_unit.duration
            })
        return trainings

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def to_representation(self):
        return dict(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            first_name=self.first_name,
            last_name=self.last_name,
            age=self.age,
            email=self.email,
            phone_number=self.phone_number,
            gender=self.gender,
            gender_label=self.get_gender_display(),
            roles=self.roles
        )


class StudentProfile(models.Model):
    # Fields
    # -------------------------------------------------------
    student = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Estudiante', limit_choices_to={'is_student': True}
    )

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'student_profile'
        verbose_name = 'Perfil de estudiante'
        verbose_name_plural = 'Perfiles de estudiantes'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.student.full_name


class UserAcademicDegree(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:
        PRIMARY_EDUCATION = "primary_education"
        SECONDARY_EDUCATION = "secondary_education"
        UNDERGRADUATE = "undergraduate"
        POSTGRADUATE = "postgraduate"
        DOCTORATE = "doctorate"

        ALL = [PRIMARY_EDUCATION, SECONDARY_EDUCATION, UNDERGRADUATE, POSTGRADUATE, DOCTORATE]

        CHOICES = (
            (PRIMARY_EDUCATION, "Educación básica"),
            (SECONDARY_EDUCATION, "Educación media"),
            (UNDERGRADUATE, "Pregrado"),
            (POSTGRADUATE, "Postgrado"),
            (DOCTORATE, "Doctorado"),
        )

    # Fields
    # -------------------------------------------------------
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    type = models.CharField("Grado", max_length=30, choices=Type.CHOICES)
    achieved_title = models.CharField("Título obtenido", max_length=300)
    study_center = models.CharField("Centro de estudios", max_length=300)
    started_at = models.DateField("Fecha de inicio")
    finished_at = models.DateField("Fecha de finalización")

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'user_academic_degree'
        verbose_name = 'Grado académico'
        verbose_name_plural = 'Grados académicos'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f"{self.user.full_name} - {self.achieved_title}"

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        return dict(
            id=self.id,
            user=self.user.id,
            type=self.type,
            type_label=self.get_type_display(),
            achieved_title=self.achieved_title,
            study_center=self.study_center,
            started_at=self.started_at,
            finished_at=self.finished_at
        )


class UserExternalTraining(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:
        TRAINING = "training"
        DIPLOMAT = "diplomat"
        COURSE = "course"
        WORKSHOP = "workshop"
        SEMINAR = "seminar"
        MODULE = "module"

        ALL = [TRAINING, DIPLOMAT, COURSE, WORKSHOP, SEMINAR, MODULE]

        CHOICES = (
            (TRAINING, "Capacitación"),
            (DIPLOMAT, "Diplomado"),
            (COURSE, "Curso"),
            (WORKSHOP, "Taller"),
            (SEMINAR, "Seminario"),
            (MODULE, "Módulo")
        )

    class Modality:
        FACE_TO_FACE = 'face_to_face'
        VIRTUAL = 'virtual'
        COMBINED = 'combined'

        CHOICES = (
            (FACE_TO_FACE, 'Presencial'),
            (VIRTUAL, 'Virtual'),
            (COMBINED, 'Presencial/Virtual')
        )

    # Fields
    # -------------------------------------------------------
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    type = models.CharField("Tipo", max_length=30, choices=Type.CHOICES)
    name = models.CharField("Nombre", max_length=150)
    description = models.CharField("Descripción", max_length=300)
    location = models.CharField("Lugar", max_length=300)
    started_at = models.DateField("Fecha de inicio")
    finished_at = models.DateField("Fecha de finalización")
    duration = models.SmallIntegerField('Duración', help_text='Duración de la capacitación en horas')
    modality = models.CharField('Modalidad', max_length=20, choices=Modality.CHOICES)
    tags = models.ManyToManyField("core.Tag", verbose_name="Temas", help_text='Área de conocimiento')

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'user_external_trainings'
        verbose_name = 'Capacitación Externa'
        verbose_name_plural = 'Capacitaciones Externas'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.name

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        return dict(
            id=self.id,
            user=self.user.id,
            type=self.type,
            type_label=self.get_type_display(),
            name=self.name,
            description=self.description,
            location=self.location,
            started_at=self.started_at,
            finished_at=self.finished_at,
            modality=self.get_modality_display(),
            duration=self.duration,
            tags=self.tags.all().values_list('display_name')
        )


class TeacherProfile(models.Model):
    # Fields
    # -------------------------------------------------------
    teacher = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Facilitador', limit_choices_to={'is_teacher': True}
    )

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'teacher_profile'
        verbose_name = 'Perfil de facilitador'
        verbose_name_plural = 'Perfiles de facilitadores'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.teacher.full_name


class OrganizationalProfile(models.Model):
    # Fields
    # -------------------------------------------------------
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuario', limit_choices_to={'is_organizational': True}
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Organización')

    # position = models.CharField('Puesto', max_length=100)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'organizational_profile'
        verbose_name = 'Perfil de usuario organizacional'
        verbose_name_plural = 'Perfiles de usuarios organizacionales'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.user.full_name
