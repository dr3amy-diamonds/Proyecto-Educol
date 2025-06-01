from django.db import models

class Curso(models.Model):
    nombre = models.CharField(max_length=200)

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
