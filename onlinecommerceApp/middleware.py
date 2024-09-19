from django.contrib.auth import logout
from django.shortcuts import redirect

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Verificar si la clave de sesión del usuario coincide con la actual
            session_key = request.user.session_key
            if session_key and session_key != request.session.session_key:
                # Si no coincide, cerrar la sesión
                logout(request)
                return redirect('login')

        response = self.get_response(request)
        return response
