# Generated by Django 4.1.3 on 2023-01-24 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='название')),
                ('capacity', models.IntegerField(verbose_name='вместимость')),
                ('city', models.CharField(max_length=25, verbose_name='город')),
            ],
            options={
                'verbose_name': 'стадион',
                'verbose_name_plural': 'стадионы',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='название')),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.stadium', verbose_name='стадион')),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='имя')),
                ('surname', models.CharField(max_length=25, verbose_name='фамилия')),
                ('power', models.PositiveSmallIntegerField(verbose_name='сила')),
                ('age', models.PositiveSmallIntegerField(verbose_name='возраст')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Свободный агент'), (1, 'Состоит в команде'), (2, 'Завершил карьеру')], default=0, verbose_name='статус')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='players', to='main.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'игрок',
                'verbose_name_plural': 'игроки',
                'ordering': ('-id',),
            },
        ),
    ]
