# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey

from training.organizations.models import Organization
from training.utils.behaviors import TimeStampedModel
from .managers import (
    CountryManager, StateManager, CountyManager, VillageManager, TrainingManager, DiplomatManager, CourseManager,
    WorkshopManager, SeminarManager, ModuleManager, AvatarResourceManager
)


class Area(MPTTModel):
    # Constants
    # -------------------------------------------------------
    class Type:
        COUNTRY = 'country'
        STATE = 'state'
        COUNTY = 'county'
        VILLAGE = 'village'

        CHOICES = (
            (COUNTRY, 'País'),
            (STATE, 'Departamento'),
            (COUNTY, 'Municipio'),
            (VILLAGE, 'Aldea')
        )

    # Fields
    # -------------------------------------------------------
    id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField('Nombre', max_length=150)
    code = models.CharField('Código', max_length=10, db_index=True)
    type = models.CharField('Tipo', max_length=15, choices=Type.CHOICES)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        unique_together = (('parent', 'code'),)

    class MPTTMeta:
        order_insertion_by = ['code']

    # Magic methods
    # -------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(Area, self).__init__(*args, **kwargs)

        if getattr(self, 'type', None):
            proxy_map = {
                self.Type.COUNTRY: Country,
                self.Type.STATE: State,
                self.Type.COUNTY: County,
                self.Type.VILLAGE: Village
            }

            self.__class__ = proxy_map.get(self.type, Area)

    def __str__(self):
        return self.name

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        return dict(id=self.id, name=self.name, code=self.code)


class Country(Area):
    # Managers
    # -------------------------------------------------------
    objects = CountryManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class State(Area):
    # Managers
    # -------------------------------------------------------
    objects = StateManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class County(Area):
    # Managers
    # -------------------------------------------------------
    objects = CountyManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'


class Village(Area):
    # Managers
    # -------------------------------------------------------
    objects = VillageManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Aldea'
        verbose_name_plural = 'Aldeas'


class Tag(TimeStampedModel):
    # Fields
    # -------------------------------------------------------
    display_name = models.CharField('Nombre', max_length=50, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.display_name


class TrainingUnit(TimeStampedModel, MPTTModel):
    # Constants
    # -------------------------------------------------------
    class Type:
        TRAINING = 'training'
        DIPLOMAT = 'diplomat'
        COURSE = 'course'
        WORKSHOP = 'workshop'
        SEMINAR = 'seminar'
        MODULE = 'module'

        # TODO: Analizar si esta es la mejor forma de manejar jerarquia por tipos
        WEIGHTS = {
            DIPLOMAT: 3,
            TRAINING: 3,
            COURSE: 2,
            WORKSHOP: 2,
            SEMINAR: 2,
            MODULE: 1
        }

        CHOICES = (
            (TRAINING, 'Capacitación'),
            (DIPLOMAT, 'Diplomado'),
            (COURSE, 'Curso'),
            (WORKSHOP, 'Taller'),
            (SEMINAR, 'Seminario'),
            (MODULE, 'Módulo')
        )

    class DifficultyLevel:
        BASIC = 'basic'
        INTERMEDIATE = 'intermediate'
        ADVANCED = 'advanced'

        CHOICES = (
            (BASIC, 'Básico'),
            (INTERMEDIATE, 'Intermedio'),
            (ADVANCED, 'Avanzado')
        )

    class SettingsKeys:
        ENROLLMENT_RULES = 'enrollment_rules'

    class ExtraDataKeys:
        REVISIONS = 'revisions'

    # Fields
    # -------------------------------------------------------
    name = models.CharField('Nombre', max_length=100)
    description = models.CharField('Descripción', max_length=300)
    content = models.TextField('Contenido', null=True, blank=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)
    order = models.SmallIntegerField('Orden', default=1)
    type = models.CharField('Tipo', max_length=20, choices=Type.CHOICES)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    duration = models.SmallIntegerField('Duración', help_text='Duración de la unidad en horas')
    difficulty_level = models.CharField('Grado de dificultad', max_length=20, choices=DifficultyLevel.CHOICES)
    tags = models.ManyToManyField(Tag, through='TrainingUnitTag')
    enabled = models.BooleanField('Habilitada?', default=True)
    """
    Examples:
        settings = {
            'enrollment_rules': {
                ...
            }
        }
    """
    settings = pg_fields.JSONField('Configuraciones', default=dict, blank=True)
    """
    Examples:
        extra_data = {
            'revisions': []
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'training_unit'
        verbose_name = 'Unidad de formación'
        verbose_name_plural = 'Unidades de formación'

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    # Magic methods
    # -------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(TrainingUnit, self).__init__(*args, **kwargs)

        if getattr(self, 'type', None):
            proxy_map = {
                self.Type.TRAINING: Training,
                self.Type.DIPLOMAT: Diplomat,
                self.Type.COURSE: Course,
                self.Type.WORKSHOP: Workshop,
                self.Type.SEMINAR: Seminar,
                self.Type.MODULE: Module
            }

            self.__class__ = proxy_map.get(self.type, TrainingUnit)

    def __str__(self):
        return self.name

    # Methods
    # -------------------------------------------------------
    def to_representation(self):
        tags = []
        tags_slugs = []
        for tag in self.tags.filter(trainingunittag__hidden=False):
            tags.append({'slug': tag.slug, 'display_name': tag.display_name})
            tags_slugs.append(tag.slug)

        return dict(
            id=self.id,
            slug=self.slug,
            name=self.name,
            description=self.description,
            content=self.content,
            type=self.type,
            type_label=self.get_type_display(),
            duration=self.duration,
            difficulty_level=self.difficulty_level,
            difficulty_level_label=self.get_difficulty_level_display(),
            tags=tags,
            tags_slugs=tags_slugs,
            sub_units=[sub_unit.to_representation() for sub_unit in self.get_children()]
        )


class Training(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = TrainingManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Capacitación'
        verbose_name_plural = 'Capacitaciones'


class Diplomat(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = DiplomatManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Diplomado'
        verbose_name_plural = 'Diplomados'


class Course(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = CourseManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Workshop(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = WorkshopManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'


class Seminar(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = SeminarManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Seminario'
        verbose_name_plural = 'Seminarios'


class Module(TrainingUnit):
    # Managers
    # -------------------------------------------------------
    objects = ModuleManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


class TrainingUnitTag(models.Model):
    # Fields
    # -------------------------------------------------------
    training_unit = models.ForeignKey(TrainingUnit, on_delete=models.CASCADE, verbose_name='Unidad de formación')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Tag')
    hidden = models.BooleanField(default=False)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'training_unit_tag'
        unique_together = ('training_unit', 'tag')

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.training_unit} - {self.tag}'


class TrainingCall(TimeStampedModel):
    # Constants
    # -------------------------------------------------------
    class Status:
        DRAFT = "draft"
        IN_REVISION = "in_revision"
        APPROVED = "approved"
        REJECTED = "rejected"
        PUBLISHED = "published"
        IN_PROGRESS = "in_progress"
        CANCELLED = "cancelled"
        SUSPENDED = "suspended"
        POSTPONED = "postponed"
        FINISHED = "finished"

        ALL = [
            DRAFT, IN_REVISION, APPROVED, REJECTED, PUBLISHED, IN_PROGRESS, CANCELLED, SUSPENDED, POSTPONED, FINISHED
        ]

        CHOICES = (
            (DRAFT, "Borrador"),
            (IN_REVISION, "En revisión"),
            (APPROVED, "Aprobado"),
            (REJECTED, "Rechazado"),
            (PUBLISHED, "Publicado"),
            (IN_PROGRESS, "En curso"),
            (CANCELLED, "Cancelado"),
            (SUSPENDED, "Suspendido"),
            (POSTPONED, "Pospuesto"),
            (FINISHED, "Finalizado")
        )

    class Type:
        SIMPLE = "simple"
        COMPOSITE = "composite"

        ALL = [SIMPLE, COMPOSITE]

        CHOICES = (
            (SIMPLE, "Convocatoria simple"),
            (COMPOSITE, "Convocatoria compuesta"),
        )

    # TODO: Determinar si es necesario el campo extra_data y de ser necesario, definir los keys
    class ExtraDataKeys:
        ENROLLMENT_FEE = 'enrollment_fee'

    # Fields
    # -------------------------------------------------------
    banner = models.ImageField("Banner", null=True, blank=True)
    thumbnail_banner = models.ImageField("Banner miniatura", null=True, blank=True)
    type = models.CharField("Tipo", max_length=30, choices=Type.CHOICES)
    slug = models.SlugField('Slug', max_length=50, unique=True)
    training_plan = models.ForeignKey(
        TrainingUnit, on_delete=models.CASCADE, verbose_name='Plan de formación', limit_choices_to={"parent": None}
    )
    status = models.CharField('Estado', max_length=30, choices=Status.CHOICES, default=Status.DRAFT, db_index=True)
    enrollment_start_date = models.DateTimeField('Fecha de inicio de inscripciones', null=True, blank=True)
    enrollment_end_date = models.DateTimeField('Fecha de finalización de inscripciones', null=True, blank=True)
    start_date = models.DateTimeField('Fecha de inicio', null=True, blank=True)
    end_date = models.DateTimeField('Fecha de finalización', null=True, blank=True)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Dueño', null=True, blank=True)
    """
    Examples:
        extra_data = {
            'enrollment_fee': 0
        }
    """
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'training_call'
        verbose_name = 'Oferta de formación'
        verbose_name_plural = 'Ofertas de formación'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return self.training_plan.name

    # Methods
    # -------------------------------------------------------
    def save(self, *args, **kwargs):
        self.slug = self.training_plan.slug
        super().save(*args, **kwargs)

    def to_representation(self):
        return dict(
            id=self.id,
            name=self.training_plan.name,
            description=self.training_plan.description,
            banner_url=self.banner.url if self.banner else None,
            status=self.status,
            status_label=self.get_status_display(),
            enrollment_start_date=str(self.enrollment_start_date),
            enrollment_end_date=str(self.enrollment_end_date),
            start_date=str(self.start_date),
            end_date=str(self.end_date),
            duration=self.training_plan.duration,
            slug=self.slug,
            type=self.type,
            type_label=self.get_type_display(),
            tags=[{"display_name": tag.display_name} for tag in self.training_plan.tags.all()]
        )


class Sponsor(models.Model):
    # Constants
    # -------------------------------------------------------
    # TODO: Determinar si es necesario el campo extra_data y de ser necesario, definir los keys
    class ExtraDataKeys:
        pass

    # Fields
    # -------------------------------------------------------
    training_call = models.ForeignKey(TrainingCall, on_delete=models.CASCADE, verbose_name='Formación')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Organización')
    extra_data = pg_fields.JSONField('Datos extra', default=dict, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'sponsor'
        verbose_name = 'Patrocinador'
        verbose_name_plural = 'Patrocinadores'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.training_call.training_plan.name} - {self.organization.name}'


class PublicLink(models.Model):
    # Fields
    # -------------------------------------------------------
    name = models.CharField('Nombre', max_length=50)
    url_path = models.URLField('Dirección web', max_length=200)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'public_link'
        verbose_name = 'Enlace'
        verbose_name_plural = 'Enlaces'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    # Fields
    # -------------------------------------------------------
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Usuario')
    position = models.CharField('Puesto', max_length=50)
    photo = models.ImageField('Foto', upload_to='team')

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'team'
        verbose_name = 'Equipo de Trabajo'
        verbose_name_plural = 'Equipo de Trabajo'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.user.full_name}'


class GeneralConfiguration(models.Model):
    # Fields
    # -------------------------------------------------------
    director_name = models.CharField('Director(a)*', max_length=100, help_text='Nombre Director(a) DGDP')
    contact_email = models.CharField('Correo de Contacto*', max_length=75)
    main_phone = models.CharField('Teléfono*', max_length=15)
    page_title = models.CharField('Título del Sitio', max_length=60, null=True, blank=True)
    site_logo = models.ImageField('Logo del Sitio', upload_to='landing_page', null=True, blank=True)
    main_photo = models.ImageField('Imagen Principal', upload_to='landing_page', null=True, blank=True)
    secondary_photo = models.ImageField('Imagen Secundaria', upload_to='landing_page', null=True, blank=True)
    welcome_message = models.TextField('Mensaje de Bienvenida', null=True, blank=True)
    favicon = models.ImageField('Icono del Sitio', upload_to='landing_page', null=True, blank=True)
    facebook_link = models.URLField('Página de Facebook', null=True, blank=True)
    youtube_link = models.URLField('Página de Youtube', null=True, blank=True)
    twitter_link = models.URLField('Página de Twitter', null=True, blank=True)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = 'general_configuration'
        verbose_name = 'Configuración General'
        verbose_name_plural = 'Configuraciones Generales'

    # Magic methods
    # -------------------------------------------------------
    def __str__(self):
        return f'{self.contact_email}'

    def clean(self, *args, **kwargs):
        model = self.__class__
        if model.objects.count() == 0 or self.id == model.objects.get().id:
            super(GeneralConfiguration, self).save(*args, **kwargs)
        else:
            raise ValidationError("Acción no permitida. Puede crearse solamente 1 Configuración.")


class Resource(models.Model):
    # Constants
    # -------------------------------------------------------
    class Type:
        AVATAR = "avatar"

        CHOICES = (
            (AVATAR, "Avatar"),
        )

    class ExtraDataKeys:
        class AvatarKeys:
            GENDER = "gender"

            class Gender:
                MALE = "male"
                FEMALE = "female"
                OTHER = "other"

    # Fields
    # -------------------------------------------------------
    name = models.CharField("Nombre", max_length=50)
    type = models.CharField("Tipo", max_length=30, choices=Type.CHOICES)
    asset = models.FileField("Recurso", max_length=200)
    """
    Examples:
        # Ejemplo de `extra_data` para `Resource` de tipo `avatar`
        extra_data: {
            "gender": "male"
        }
    """
    extra_data = pg_fields.JSONField("Extra data", default=dict)

    # Meta
    # -------------------------------------------------------
    class Meta:
        db_table = "resource"
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"

    # Magic methods
    # -------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

        if getattr(self, 'type', None):
            proxy_map = {
                self.Type.AVATAR: AvatarResource,
            }

            self.__class__ = proxy_map.get(self.type, Resource)

    def __str__(self):
        return self.name


class AvatarResource(Resource):
    # Managers
    # -------------------------------------------------------
    objects = AvatarResourceManager()

    # Meta
    # -------------------------------------------------------
    class Meta:
        proxy = True
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'

    # Properties
    # -------------------------------------------------------
    @property
    def gender(self):
        return self.extra_data.get(self.ExtraDataKeys.AvatarKeys.GENDER, self.ExtraDataKeys.AvatarKeys.Gender.OTHER)
