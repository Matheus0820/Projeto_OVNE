# Generated by Django 4.2.4 on 2024-01-18 00:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0014_alter_materias_publicacao_alter_videos_publicacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materias',
            name='publicacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 21, 1, 16, 22949)),
        ),
        migrations.AlterField(
            model_name='videos',
            name='publicacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 17, 21, 1, 16, 21955)),
        ),
    ]