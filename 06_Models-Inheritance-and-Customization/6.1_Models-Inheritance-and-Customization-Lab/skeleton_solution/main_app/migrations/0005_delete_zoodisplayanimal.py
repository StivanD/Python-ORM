# Generated by Django 5.0.4 on 2024-07-16 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_rename_zoodisplayanimals_zoodisplayanimal'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ZooDisplayAnimal',
        ),
    ]
