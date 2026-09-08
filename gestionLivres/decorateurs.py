from django.http import HttpResponseForbidden

def adminRequired(view_func):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'is_admin', False):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Accès refusé : Vous devez être administrateur pour accéder à cette page."
        )
    return wrapper