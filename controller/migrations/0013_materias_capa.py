# Generated by Django 4.2.4 on 2023-12-18 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0012_remove_materias_capa'),
    ]

    operations = [
        migrations.AddField(
            model_name='materias',
            name='capa',
            field=models.ImageField(default=None, upload_to='capas'),
        ),
    ]
