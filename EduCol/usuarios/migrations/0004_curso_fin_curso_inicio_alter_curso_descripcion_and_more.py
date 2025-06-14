# Generated by Django 5.2.1 on 2025-05-29 04:16

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_libro'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='fin',
            field=models.DateField(default=datetime.date(2025, 12, 31)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curso',
            name='inicio',
            field=models.DateField(default=datetime.date(2025, 12, 31)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curso',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='estudiantes',
            field=models.ManyToManyField(blank=True, related_name='cursos_inscritos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulos', to='usuarios.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('fecha_entrega', models.DateField()),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades', to='usuarios.modulo')),
            ],
        ),
        migrations.CreateModel(
            name='ProfesorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='profesores/cv/')),
                ('certificados', models.FileField(upload_to='profesores/certificados/')),
                ('identidad', models.FileField(upload_to='profesores/identidad/')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='profesores/fotos/')),
                ('biografia', models.TextField(blank=True)),
                ('linkedin', models.URLField(blank=True)),
                ('especialidades', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_profesor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
