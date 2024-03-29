from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
)
from app.decorators.admin_required import admin_required
from app.decorators.owner_required import owner_required
from flask_login import login_required, current_user
from sqlalchemy import not_, asc
from app.models.Votacion import Votacion
from app.models.Usuario import Usuario
from app.models.Estado import Estado
from app.models.Sancion import Sancion
from app import db
import json
from app.routes.administrador_routes import carga_config


bp = Blueprint("sancion", __name__)


@bp.route("/Sanciones", methods=["POST", "GET"])
@login_required
@admin_required
@owner_required
def view_sanciones():
    usuarios = Usuario.query.filter(~Usuario.idRol.in_([3, 4])).all()
    sanciones = Sancion.query.order_by(Sancion.idSancion.desc()).all()
    config = carga_config()

    return render_template(
        "sanciones/index.html", usuarios=usuarios, sanciones=sanciones, config=config
    )


@bp.route("/buscar/sanciones", methods=["POST"])
def buscar_by_usuario():
    data = request.json

    documentoUsuario = data["documentoUsuario"]
    usuario = Usuario.query.filter_by(documentoUsuario=documentoUsuario).first()
    if not usuario:
        return {"rs": 404, "rz": "usuario"}

    sanciones = Sancion.query.filter_by(idUsuario=usuario.idUsuario).all()
    sanciones_dict = []
    for sancion in sanciones:
        sancion = {"idSancion": sancion.idSancion}
        sanciones_dict.append(sancion)

    if not sanciones:
        return {"rs": 404, "rz": "sancion"}

    return {"rs": 200, "sanciones": sanciones_dict}
