from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario

from app import db


bp = Blueprint("administrador", __name__)



@bp.route("/Administrar")
@login_required
def inicio_administrador():
    if not isAdmin():
        return redirect(url_for('general.inicio'))
    return render_template('administrador/index.html')









def isAdmin():
    rs = session["rolUsuario"]['idRol'] == 36 or session["rolUsuario"]['idRol'] == 35    
    return rs