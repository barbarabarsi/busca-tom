# Generated by Django 4.0.5 on 2022-07-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tom_app', '0002_remove_musica_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='musica',
            name='nome',
            field=models.CharField(default='', max_length=255),
        ),
    ]