# Generated by Django 4.1.3 on 2022-12-28 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_stadium_capacity_alter_stadium_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='stadium',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.stadium', verbose_name='стадион команды'),
        ),
    ]
