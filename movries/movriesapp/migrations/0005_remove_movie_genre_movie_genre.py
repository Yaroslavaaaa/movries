# Generated by Django 4.2.7 on 2023-12-09 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movriesapp', '0004_country_alter_movie_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='movriesapp.genres', verbose_name='Жанр'),
        ),
    ]
