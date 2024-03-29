# Generated by Django 2.1.1 on 2019-03-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190322_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingcall',
            name='description',
        ),
        migrations.RemoveField(
            model_name='trainingcall',
            name='name',
        ),
        migrations.RemoveField(
            model_name='trainingunit',
            name='status',
        ),
        migrations.AddField(
            model_name='trainingcall',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Banner'),
        ),
        migrations.AddField(
            model_name='trainingcall',
            name='thumbnail_banner',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Banner miniatura'),
        ),
        migrations.AlterField(
            model_name='trainingcall',
            name='status',
            field=models.CharField(choices=[('draft', 'Borrador'), ('in_revision', 'En revisión'), ('approved', 'Aprobado'), ('rejected', 'Rechazado'), ('published', 'Publicado'), ('in_progress', 'En curso'), ('cancelled', 'Cancelado'), ('suspended', 'Suspendido'), ('postponed', 'Pospuesto'), ('finished', 'Finalizado')], db_index=True, default='draft', max_length=30, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='trainingunit',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Contenido'),
        ),
        migrations.AlterField(
            model_name='trainingunit',
            name='order',
            field=models.SmallIntegerField(default=1, verbose_name='Orden'),
        ),
    ]
