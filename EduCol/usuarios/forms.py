from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Libro
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, ProfesorProfile

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label="Contraseña",
        required=True
    )

    class Meta:
        model = User
        fields = ("nombre_completo", "mail", "password")

    def clean_mail(self):
        mail = self.cleaned_data.get('mail')
        if User.objects.filter(mail=mail).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return mail

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # encripta la contraseña
        if commit:
            user.save()
        return user
    
class LibroForm(forms.ModelForm):
    class Meta:
        model  = Libro
        fields = ['titulo','autor','area','enlace','portada']



from .models import Usuario, Libro, ProfesorProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProfesorProfile

User = get_user_model()

class ProfesorRegisterForm(forms.Form):
    # Datos de AbstractUser
    nombre_completo = forms.CharField()
    mail            = forms.EmailField()
    password1       = forms.CharField(widget=forms.PasswordInput)
    password2       = forms.CharField(widget=forms.PasswordInput)

    # Datos de perfil
    nivel_educativo = forms.CharField()
    titulo          = forms.CharField()
    institucion     = forms.CharField()
    experiencia     = forms.IntegerField(min_value=0)
    curso_dictar = forms.ChoiceField(
        label="Cursos a dictar",
        choices=Libro.AREAS
    )
    nivel_curso     = forms.ChoiceField(choices=[('Básico','Básico'),('Intermedio','Intermedio'),('Avanzado','Avanzado')])
    modalidad       = forms.ChoiceField(choices=[('Presencial','Presencial'),('Virtual','Virtual'),('Híbrido','Híbrido')])
    horario         = forms.CharField()
    carga           = forms.CharField()
    cv              = forms.FileField()
    certificados    = forms.FileField()
    identidad       = forms.FileField()
    acepta_terminos = forms.BooleanField()
    consiente_datos = forms.BooleanField()
    foto_perfil     = forms.ImageField(required=False)
    biografia       = forms.CharField(widget=forms.Textarea, required=False)
    linkedin        = forms.URLField(required=False)
    especialidades  = forms.CharField(required=False)



    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            'mail', 'telefono', 'nivel_educativo', 'titulo_profesional',
            'institucion', 'experiencia', 'curso_dictar', 'nivel_curso',
            'modalidad', 'horario', 'carga', 'cv', 'certificados',
            'identidad', 'foto_perfil', 'biografia', 'linkedin',
            'especialidades', 'password1', 'password2'
        ]
