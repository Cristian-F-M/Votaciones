from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.decorators.admin_required import admin_required
from app.decorators.owner_required import owner_required
from app import db


bp = Blueprint("tipoDocumento", __name__)


@bp.route("/Add/TipoDocumento", methods=["POST"])
@login_required
@admin_required
@owner_required
def add_tipoDocumento():
    descripcionTipoDocumento = request.form["descripcionTipoDocumento"]

    new_tipoDocumento = TipoDocumento(descripcionTipoDocumento=descripcionTipoDocumento)

    db.session.add(new_tipoDocumento)
    db.session.commit()
    flash(["informacion", "Se añadio un nuevo tipo de documento"], "session")
    return redirect(url_for("administrador.view_complementos", tag="tipoDocumento"))


@bp.route("/Delete/TipoDocumento/<int:tipoDocumento>", methods=["POST"])
@login_required
@admin_required
@owner_required
def delete_tipoDocumento(tipoDocumento):

    tipoDocumento = TipoDocumento.query.get_or_404(tipoDocumento)
    db.session.delete(tipoDocumento)

    db.session.commit()
    flash(["informacion", "Se elimino este tipo de documento"], "session")
    return redirect(url_for("administrador.view_complementos", tag="tipoDocumento"))


@bp.route("/Edit/TipoDocumento/<int:tipoDocumento>", methods=["POST"])
@login_required
@admin_required
@owner_required
def edit_tipoDocumento(tipoDocumento):

    tipoDocumento = TipoDocumento.query.get_or_404(tipoDocumento)
    tipoDocumento.descripcionTipoDocumento = request.form["descripcionTipoDocumento"]

    db.session.commit()

    flash(["informacion", "Se Actualizado este tipo de documento"], "session")
    return redirect(url_for("administrador.view_complementos", tag="tipoDocumento"))
