from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.Rol import Rol
from app.decorators.admin_required import admin_required
from app.decorators.owner_required import owner_required
from app import db


bp = Blueprint("rol", __name__)


@bp.route("/Add/Rol", methods=["POST"])
@login_required
@admin_required
@owner_required
def add_rol():
    descripcionRol = request.form["descripcionRol"]

    new_rol = Rol(descripcionRol=descripcionRol)

    db.session.add(new_rol)
    db.session.commit()
    flash(["informacion", "Se añadio un nuevo rol"], "session")
    return redirect(url_for("administrador.view_complementos", tag="rol"))


@bp.route("/Delete/Rol/<int:rol>", methods=["POST"])
@login_required
@admin_required
@owner_required
def delete_rol(rol):
    rol = Rol.query.get_or_404(rol)
    db.session.delete(rol)

    db.session.commit()
    flash(["informacion", "Se elimino este rol"], "session")
    return redirect(url_for("administrador.view_complementos", tag="rol"))


@bp.route("/Edit/Rol/<int:rol>", methods=["POST"])
@login_required
@admin_required
@owner_required
def edit_rol(rol):

    rol = Rol.query.get_or_404(rol)
    rol.descripcionRol = request.form['descripcionRol']
    
    db.session.commit()
    
    flash(["informacion", "Se Actualizado este rol"], "session")
    return redirect(url_for("administrador.view_complementos", tag="rol"))
