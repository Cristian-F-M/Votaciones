from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.Estado import Estado
from app.decorators.admin_required import admin_required
from app.decorators.owner_required import owner_required
from app import db


bp = Blueprint("estado", __name__)


@bp.route("/Add/Estado", methods=["POST"])
@login_required
@admin_required
@owner_required
def add_estado():
    descripcionEstado = request.form["descripcionEstado"]

    new_estado = Estado(descripcionEstado=descripcionEstado)

    db.session.add(new_estado)
    db.session.commit()
    flash(["informacion", "Se añadio un nuevo estado"], "session")
    return redirect(url_for("administrador.view_complementos", tag="estado"))


@bp.route("/Delete/Estado/<int:estado>", methods=["POST"])
@login_required
@admin_required
@owner_required
def delete_estado(estado):

    estado = Estado.query.get_or_404(estado)
    db.session.delete(estado)

    db.session.commit()
    flash(["informacion", "Se elimino este estado"], "session")
    return redirect(url_for("administrador.view_complementos", tag="estado"))


@bp.route("/Edit/Estado/<int:estado>", methods=["POST"])
@login_required
@admin_required
@owner_required
def edit_estado(estado):

    estado = Estado.query.get_or_404(estado)
    estado.descripcionEstado = request.form['descripcionEstado']
    
    db.session.commit()
    
    flash(["informacion", "Se Actualizado este estado"], "session")
    return redirect(url_for("administrador.view_complementos", tag="estado"))
