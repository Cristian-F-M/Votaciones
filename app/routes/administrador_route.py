from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion

from app import db


bp = Blueprint("administrador", __name__)


@bp.route("/Administrar")
@login_required
def inicio_administrador():
    if not isAdmin():
        return redirect(url_for("general.inicio"))
    return render_template("administrador/index.html")


@bp.route("/Votaciones")
@login_required
def votaciones():
    if not isAdmin():
        return redirect(url_for("general.inicio"))

    votaciones = Votacion.query.all()
    rpActual = Votacion.query.filter(Votacion.ganadorVotacion != None).first()
    return render_template("administrador/votaciones.html", votaciones=votaciones, rpActual=rpActual)


def isAdmin():
    rs = current_user.rolUsuario.idRol == 36 or current_user.rolUsuario.idRol == 35
    return rs
