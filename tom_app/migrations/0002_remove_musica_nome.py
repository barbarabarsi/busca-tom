# Generated by Django 4.0.5 on 2022-07-14 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tom_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musica',
            name='nome',
        ),
    ]
