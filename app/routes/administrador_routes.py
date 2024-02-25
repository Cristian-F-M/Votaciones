from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from sqlalchemy import desc
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion
from app.models.Estado import Estado
from app.models.Rol import Rol
from app.decorators.admin_required import admin_required
from app.decorators.owner_required import owner_required
from app import db
import json

bp = Blueprint("administrador", __name__)


@bp.route("/Administrar")
@login_required
@admin_required
def view_home():
    config = carga_config()
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    return render_template("administrador/index.html", usuarios=usuarios, config=config)


@bp.route("/Votaciones")
@login_required
@admin_required
def view_votes():
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    votaciones = Votacion.query.order_by(desc(Votacion.idVotacion)).all()
    rpActual = Votacion.query.order_by(desc(Votacion.idVotacion)).first()
    config = carga_config()

    return render_template(
        "administrador/votes.html",
        votaciones=votaciones,
        rpActual=rpActual,
        usuarios=usuarios,
        config=config,
    )


@bp.route("/Aprendices")
@login_required
@admin_required
def view_aprendices():
    aprendices = Usuario.query.filter_by(idRol=1).all()
    usuariosAll = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    tiposDocumento = TipoDocumento.query.all()
    config = carga_config()

    return render_template(
        "administrador/aprendices.html",
        aprendices=aprendices,
        usuariosAll=usuariosAll,
        tiposDocumento=tiposDocumento,
        config=config,
    )


@bp.route("/Usuarios")
@login_required
@admin_required
@owner_required
def view_usuarios():
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    usuariosAll = Usuario.query.filter(~Usuario.idRol.in_([4])).all()
    tiposDocumento = TipoDocumento.query.all()
    config = carga_config()

    return render_template(
        "administrador/usuarios.html",
        usuarios=usuarios,
        usuariosAll=usuariosAll,
        tiposDocumento=tiposDocumento,
        config=config,
    )


@bp.route("/Complementos")
@login_required
@admin_required
@owner_required
def view_complementos():
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    estados = Estado.query.all()
    tiposDocumento = TipoDocumento.query.all()
    roles = Rol.query.all()
    config = carga_config()

    return render_template(
        "administrador/complementos.html",
        usuarios=usuarios,
        estados=estados,
        tiposDocumento=tiposDocumento,
        roles=roles,
        config=config,
    )


@bp.route("/add/admin/<int:usuario>", methods=["POST"])
@login_required
@admin_required
@owner_required
def add_admin(usuario):
    usuario = Usuario.query.get_or_404(usuario)
    usuario.idRol = 3
    db.session.commit()
    flash(["informacion", "El usuario ahora es administrador"], "session")
    return redirect(url_for("administrador.view_usuarios"))


@bp.route("/remove/admin/<int:usuario>", methods=["POST"])
@login_required
@admin_required
@owner_required
def remove_admin(usuario):
    usuario = Usuario.query.get_or_404(usuario)
    usuario.idRol = 1
    db.session.commit()

    flash(["informacion", "El usuario ya no es administrador"], "session")
    return redirect(url_for("administrador.view_usuarios"))


@bp.route("/Edit/Config/<string:url>", methods=["POST"])
@login_required
@admin_required
@owner_required
def edit_config(url):

    correosInicioVotacion = request.form.get("correosInicioVotacion", "off")
    correosFinVotacion = request.form.get("correosFinVotacion", "off")
    correosSancionesVotacion = request.form.get("correosSancionesVotacion", "off")

    correosInicioVotacion = True if correosInicioVotacion == "on" else False
    correosFinVotacion = True if correosFinVotacion == "on" else False
    correosSancionesVotacion = True if correosSancionesVotacion == "on" else False

    config = carga_config()

    nueva_config = {
        "correosInicioVotacion": correosInicioVotacion,
        "correosFinVotacion": correosFinVotacion,
        "correosSancionesVotacion": correosSancionesVotacion,
    }

    config.update(nueva_config)

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    url = f"/{url}"

    flash(["informacion", "La configuraciones se actualizaron correctamente"], "session")
    return redirect(url)


def carga_config():
    with open("config.json") as f:
        config = json.load(f)
        return config
