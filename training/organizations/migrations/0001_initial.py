# Generated by Django 2.1.1 on 2019-03-03 03:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=30, verbose_name='Creado por')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_by', models.CharField(default='', max_length=30, verbose_name='Última modificación por')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última modificación el')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('code', models.CharField(max_length=10, verbose_name='Código')),
                ('type', models.CharField(choices=[('regional_center', 'Centro Regional'), ('ngo', 'ONG'), ('departmental', 'Departamental'), ('district', 'Distrital')], max_length=30, verbose_name='Tipo')),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Datos extra')),
            ],
            options={
                'verbose_name': 'Organización',
                'verbose_name_plural': 'Organizaciones',
                'db_table': 'organization',
            },
        ),
        migrations.CreateModel(
            name='OrganizationArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Area', verbose_name='Area')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='Organización')),
            ],
            options={
                'db_table': 'organization_area',
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='jurisdiction',
            field=models.ManyToManyField(through='organizations.OrganizationArea', to='core.Area'),
        ),
        migrations.CreateModel(
            name='Departmental',
            fields=[
            ],
            options={
                'verbose_name': 'Departamental',
                'verbose_name_plural': 'Departamentales',
                'proxy': True,
                'indexes': [],
            },
            bases=('organizations.organization',),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
            ],
            options={
                'verbose_name': 'Distrital',
                'verbose_name_plural': 'Distritales',
                'proxy': True,
                'indexes': [],
            },
            bases=('organizations.organization',),
        ),
        migrations.CreateModel(
            name='NGO',
            fields=[
            ],
            options={
                'verbose_name': 'Organización no gubernamental',
                'verbose_name_plural': 'Organizaciones no gubernamentales',
                'proxy': True,
                'indexes': [],
            },
            bases=('organizations.organization',),
        ),
        migrations.CreateModel(
            name='RegionalCenter',
            fields=[
            ],
            options={
                'verbose_name': 'Centro regional',
                'verbose_name_plural': 'Centros regionales',
                'proxy': True,
                'indexes': [],
            },
            bases=('organizations.organization',),
        ),
    ]
