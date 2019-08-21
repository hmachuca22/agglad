# Generated by Django 2.1.1 on 2019-03-22 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190313_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEmployeeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('type', models.CharField(choices=[('teacher', 'Docente'), ('administrative', 'Administrativo')], max_length=30, verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Tipo de Empleado',
                'verbose_name_plural': 'Tipos de Empleados',
                'db_table': 'employee_type',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='residence_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_user', to='core.Area', verbose_name='Lugar de residencia'),
        ),
    ]
