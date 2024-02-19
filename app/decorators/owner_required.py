from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def owner_required(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        if current_user.is_authenticated and current_user.rolUsuario.idRol == 4:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("administrador.view_home"))

    return decorador
