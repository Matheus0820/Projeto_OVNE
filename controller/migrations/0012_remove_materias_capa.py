# Generated by Django 4.2.4 on 2023-12-18 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0011_materias_capa_alter_materias_publicacao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materias',
            name='capa',
        ),
    ]