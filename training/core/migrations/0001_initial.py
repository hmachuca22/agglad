# Generated by Django 2.1.1 on 2019-03-03 03:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('code', models.CharField(db_index=True, max_length=10, verbose_name='Código')),
                ('type', models.CharField(choices=[('country', 'País'), ('state', 'Departamento'), ('county', 'Municipio'), ('village', 'Aldea')], max_length=15, verbose_name='Tipo')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='GeneralConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_email', models.CharField(max_length=75, verbose_name='Correo de Contacto*')),
                ('main_phone', models.CharField(max_length=15, verbose_name='Teléfono*')),
                ('page_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Título del Sitio')),
                ('site_logo', models.ImageField(blank=True, null=True, upload_to='landing_page', verbose_name='Logo del Sitio')),
                ('main_photo', models.ImageField(blank=True, null=True, upload_to='landing_page', verbose_name='Imagen Principal')),
                ('secondary_photo', models.ImageField(blank=True, null=True, upload_to='landing_page', verbose_name='Imagen Secundaria')),
                ('welcome_message', models.TextField(blank=True, null=True, verbose_name='Mensaje de Bienvenida')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='landing_page', verbose_name='Icono del Sitio')),
                ('facebook_link', models.URLField(blank=True, null=True, verbose_name='Página de Facebook')),
                ('youtube_link', models.URLField(blank=True, null=True, verbose_name='Página de Youtube')),
                ('twitter_link', models.URLField(blank=True, null=True, verbose_name='Página de Twitter')),
            ],
            options={
                'verbose_name': 'Configuración General',
                'verbose_name_plural': 'Configuraciones Generales',
                'db_table': 'general_configuration',
            },
        ),
        migrations.CreateModel(
            name='PublicLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('url_path', models.URLField(verbose_name='Dirección web')),
            ],
            options={
                'verbose_name': 'Enlace',
                'verbose_name_plural': 'Enlaces',
                'db_table': 'public_link',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('type', models.CharField(choices=[('avatar', 'Avatar')], max_length=30, verbose_name='Tipo')),
                ('asset', models.FileField(max_length=200, upload_to='', verbose_name='Recurso')),
            ],
            options={
                'verbose_name': 'Recurso',
                'verbose_name_plural': 'Recursos',
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Datos extra')),
            ],
            options={
                'verbose_name': 'Patrocinador',
                'verbose_name_plural': 'Patrocinadores',
                'db_table': 'sponsor',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=30, verbose_name='Creado por')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_by', models.CharField(default='', max_length=30, verbose_name='Última modificación por')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última modificación el')),
                ('display_name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50, verbose_name='Puesto')),
                ('photo', models.ImageField(upload_to='team', verbose_name='Foto')),
            ],
            options={
                'verbose_name': 'Equipo de Trabajo',
                'verbose_name_plural': 'Equipo de Trabajo',
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='TrainingCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=30, verbose_name='Creado por')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_by', models.CharField(default='', max_length=30, verbose_name='Última modificación por')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última modificación el')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Descripción')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('status', models.CharField(choices=[('scheduled', 'Programado'), ('in_progress', 'En curso'), ('cancelled', 'Cancelado'), ('suspended', 'Suspendido'), ('postponed', 'Pospuesto'), ('finished', 'Finalizado')], db_index=True, default='scheduled', max_length=30, verbose_name='Estado')),
                ('enrollment_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio de inscripciones')),
                ('enrollment_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de finalización de inscripciones')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de finalización')),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Datos extra')),
            ],
            options={
                'verbose_name': 'Oferta de formación',
                'verbose_name_plural': 'Ofertas de formación',
                'db_table': 'training_call',
            },
        ),
        migrations.CreateModel(
            name='TrainingUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=30, verbose_name='Creado por')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_by', models.CharField(default='', max_length=30, verbose_name='Última modificación por')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última modificación el')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(max_length=300, verbose_name='Descripción')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('order', models.SmallIntegerField(verbose_name='Orden')),
                ('type', models.CharField(choices=[('training', 'Capacitación'), ('diplomat', 'Diplomado'), ('course', 'Curso'), ('workshop', 'Taller'), ('seminar', 'Seminario'), ('module', 'Módulo')], max_length=20, verbose_name='Tipo')),
                ('duration', models.SmallIntegerField(help_text='Duración de la unidad en horas', verbose_name='Duración')),
                ('difficulty_level', models.CharField(choices=[('basic', 'Básico'), ('intermediate', 'Intermedio'), ('advanced', 'Avanzado')], max_length=20, verbose_name='Grado de dificultad')),
                ('status', models.CharField(choices=[('draft', 'Borrador'), ('in_review', 'En revisión'), ('rejected', 'Rechazado'), ('approved', 'Aprobado')], default='draft', max_length=30, verbose_name='Estado')),
                ('enabled', models.BooleanField(default=True, verbose_name='Habilitada?')),
                ('settings', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Configuraciones')),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Datos extra')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.TrainingUnit')),
            ],
            options={
                'verbose_name': 'Unidad de formación',
                'verbose_name_plural': 'Unidades de formación',
                'db_table': 'training_unit',
            },
        ),
        migrations.CreateModel(
            name='TrainingUnitTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hidden', models.BooleanField(default=False)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Tag', verbose_name='Tag')),
                ('training_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TrainingUnit', verbose_name='Unidad de formación')),
            ],
            options={
                'db_table': 'training_unit_tag',
            },
        ),
        migrations.AddField(
            model_name='trainingunit',
            name='tags',
            field=models.ManyToManyField(through='core.TrainingUnitTag', to='core.Tag'),
        ),
    ]