# Generated by Django 2.1.1 on 2019-03-14 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190309_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalconfiguration',
            name='director_name',
            field=models.CharField(default='Lic. Lucidalia Carranza', max_length=100, verbose_name='Nombre Director(a) DGDP*'),
            preserve_default=False,
        ),
    ]