# Generated by Django 2.1.1 on 2019-09-02 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190821_2215'),
        ('users', '0008_auto_20190619_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dependencia_se',
            field=models.CharField(blank=True, choices=[('Centro Educativo', 'Centro Educativo'), ('Dirección Distrital', 'Dirección Distrital'), ('Departamental', 'Departamental'), ('Centro Regional', 'Centro Regional')], max_length=60, null=True, verbose_name='Dependencia SE'),
        ),
        migrations.AddField(
            model_name='userexternaltraining',
            name='age',
            field=models.SmallIntegerField(blank=True, help_text='Edad participante', null=True, verbose_name='Edad participante'),
        ),
        migrations.AddField(
            model_name='userexternaltraining',
            name='area_educativa',
            field=models.CharField(blank=True, choices=[('Ciencias Naturales', 'Ciencias Naturales'), ('Ciencias Sociales', 'Ciencias Sociales'), ('Comunicación', 'Comunicación'), ('Educación Física', 'Educación Física'), ('Gestión Educativa', 'Gestión Educativa'), ('Innovación Tecnológica', 'Innovación Tecnológica'), ('Investigación Educativa', 'Investigación Educativa'), ('Matemática', 'Matemática'), ('Tecnología', 'Tecnología')], max_length=80, null=True, verbose_name='Area'),
        ),
        migrations.AddField(
            model_name='userexternaltraining',
            name='nivel_educativo',
            field=models.CharField(blank=True, choices=[('Prebásico', 'Prebásico'), ('Básico', 'Básico'), ('Medio', 'Medio')], max_length=30, null=True, verbose_name='Nivel Educativo'),
        ),
        migrations.AddField(
            model_name='userexternaltraining',
            name='training_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ext_training_place', to='core.Area', verbose_name='Lugar de capacitación'),
        ),
        migrations.AlterField(
            model_name='userexternaltraining',
            name='modality',
            field=models.CharField(choices=[('face_to_face', 'Presencial'), ('virtual', 'Virtual'), ('combined', 'Mixta')], max_length=20, verbose_name='Modalidad'),
        ),
        migrations.AlterField(
            model_name='userexternaltraining',
            name='type',
            field=models.CharField(choices=[('training', 'Capacitación'), ('diplomat', 'Diplomado'), ('course', 'Curso'), ('workshop', 'Taller'), ('seminar', 'Seminario'), ('module', 'Módulo'), ('publication', 'Publicación')], max_length=30, verbose_name='Tipo'),
        ),
    ]
