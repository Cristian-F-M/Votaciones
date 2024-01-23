from flask import Blueprint, render_template
from flask_login import login_required
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario

from app import db


bp = Blueprint("general", __name__)


@bp.route("/")
def login():
    TiposDocumento = TipoDocumento.query.all()
    return render_template("auth/login.html", TiposDocumento=TiposDocumento)


@bp.route("/registro")
def register():
    TiposDocumento = TipoDocumento.query.all()
    return render_template("auth/registro.html", TiposDocumento=TiposDocumento)


@bp.route("/inicio")
@login_required
def inicio():
    return render_template("index.html")


@bp.route("/Votar")
@login_required
def votar():
    candidatos = Usuario.query.filter_by(idRol=2).all()
    return render_template("votar.html", candidatos=candidatos)

