from flask import Blueprint, render_template, session, redirect, url_for, g
from sqlalchemy import desc
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion
from app.decorators.admin_required import admin_required

from app import db


bp = Blueprint("administrador", __name__)


@bp.route("/Administrar")
@login_required
@admin_required
def view_home():
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    g.usuarios = usuarios
    return render_template("administrador/index.html")


@bp.route("/Votaciones")
@login_required
@admin_required
def view_votes():
    votaciones = Votacion.query.order_by(desc(Votacion.idVotacion)).all()
    rpActual = Votacion.query.order_by(desc(Votacion.idVotacion)).first()
    return render_template(
        "administrador/votes.html", votaciones=votaciones, rpActual=rpActual
    )
