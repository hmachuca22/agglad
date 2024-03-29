# Generated by Django 2.1.1 on 2019-06-19 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190326_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'avatar'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Resource', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Número de teléfono'),
        ),
        migrations.AlterField(
            model_name='user',
            name='residence_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area_user', to='core.Area', verbose_name='Lugar de residencia'),
        ),
    ]
