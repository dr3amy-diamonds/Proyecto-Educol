from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.conf import settings

class UsuarioManager(BaseUserManager):
    def create_user(self, mail, password=None, **extra_fields):
        extra_fields.pop('username', None)  # <-- Esta línea es clave
        if not mail:
            raise ValueError('El correo electrónico es obligatorio')
        mail = self.normalize_email(mail)
        user = self.model(mail=mail, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail, password=None, **extra_fields):
        extra_fields.pop('username', None)  # <-- Esta línea también
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mail, password, **extra_fields)

class Usuario(AbstractUser):
    es_estudiante = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)
    
    username = None  # Eliminamos el campo username

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['nombre_completo']

    nombre_completo = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    groups = models.ManyToManyField(Group, related_name="usuarios_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="usuarios_permissions")

    objects = UsuarioManager()  # <-- Aquí asignamos el manager

class ProfesorProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL,
                                           on_delete=models.CASCADE,
                                           related_name='perfil_profesor')
    cv              = models.FileField(upload_to='profesores/cv/')
    certificados    = models.FileField(upload_to='profesores/certificados/')
    identidad       = models.FileField(upload_to='profesores/identidad/')
    foto_perfil     = models.ImageField(upload_to='profesores/fotos/', blank=True, null=True)
    biografia       = models.TextField(blank=True)
    linkedin        = models.URLField(blank=True)
    especialidades  = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.mail}"
    

# usuarios/migrations/0002_create_profesores_group.py
from django.db import migrations

def create_profesores_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Profesores')

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_profesores_group),
    ]



class Libro(models.Model):
    AREAS = [
        ('Matemáticas', 'Matemáticas'),
        ('Ciencias Naturales', 'Ciencias Naturales'),
        ('Lenguaje', 'Lenguaje'),
        ('Humanidades', 'Humanidades'),
        ('Informática', 'Informática'),
    ]

    titulo  = models.CharField(max_length=200)
    autor   = models.CharField(max_length=100, blank=True)
    area    = models.CharField(max_length=50, choices=AREAS)
    enlace  = models.URLField(blank=True)
    portada = models.ImageField(upload_to='portadas/', blank=True)

    def __str__(self):
        return self.titulo
    
class Curso(models.Model):
    nombre       = models.CharField(max_length=200)
    descripcion  = models.TextField(blank=True)
    profesor     = models.ForeignKey(
                      Usuario,
                      on_delete=models.CASCADE,
                      related_name="cursos_creados"
                   )
    estudiantes  = models.ManyToManyField(
                      Usuario,
                      related_name="cursos_inscritos",
                      blank=True
                   )
    inicio       = models.DateField()
    fin          = models.DateField()

    def __str__(self):
        return self.nombre


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=100)
    inicio = models.DateField()
    fin    = models.DateField()

    def __str__(self):
        return f"{self.curso.nombre} · {self.titulo}"

class Actividad(models.Model):
    modulo        = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='actividades')
    titulo        = models.CharField(max_length=200)
    fecha_entrega = models.DateField()

    def __str__(self):
        return f"{self.modulo.titulo}: {self.titulo}"

class ProfesorProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesor_profile')
    nivel_educativo = models.CharField(max_length=100)
    titulo          = models.CharField(max_length=100)
    institucion     = models.CharField(max_length=200)
    experiencia     = models.PositiveIntegerField()
    curso_dictar    = models.CharField(max_length=100)
    nivel_curso     = models.CharField(max_length=50)
    modalidad       = models.CharField(max_length=50)
    horario         = models.CharField(max_length=100)
    carga           = models.CharField(max_length=100)
    cv              = models.FileField(upload_to='profesores/cv/')
    certificados    = models.FileField(upload_to='profesores/certificados/')
    identidad       = models.FileField(upload_to='profesores/identidad/')
    acepta_terminos = models.BooleanField(default=False)
    consiente_datos = models.BooleanField(null=True, blank=True)
    foto_perfil     = models.ImageField(upload_to='profesores/fotos/', blank=True, null=True)
    biografia       = models.TextField(blank=True)
    linkedin        = models.URLField(blank=True)
    especialidades  = models.CharField(max_length=200, blank=True)
    
