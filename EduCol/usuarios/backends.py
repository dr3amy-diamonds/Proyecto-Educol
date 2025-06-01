from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Autenticación usando el campo 'mail' en lugar de 'username'.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(mail=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
