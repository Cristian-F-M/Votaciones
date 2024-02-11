from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def admin_required(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        if current_user.is_authenticated and (
            current_user.rolUsuario.idRol == 3 or current_user.rolUsuario.idRol == 4
        ):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("usuario.view_home"))

    return decorador
