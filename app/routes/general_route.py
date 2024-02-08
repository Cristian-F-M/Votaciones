from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import not_, asc
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sqlalchemy.orm import aliased
from datetime import datetime


from app import db


bp = Blueprint("general", __name__)


@bp.route("/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("administrador.inicio_administrador"))

    TiposDocumento = TipoDocumento.query.all()
    return render_template("auth/login.html", TiposDocumento=TiposDocumento)


@bp.route("/registro")
def register():
    TiposDocumento = TipoDocumento.query.all()
    return render_template("auth/registro.html", TiposDocumento=TiposDocumento)


@bp.route("/inicio")
@login_required
def inicio():
    ultimaVotacion = Votacion.query.first()
    return render_template("index.html", votacion=ultimaVotacion)


@bp.route("/Votar")
@login_required
def votar():
    ultimaVotacion = Votacion.query.first()
    candidatos = Usuario.query.filter_by(idRol=34).all()
    return render_template("votar.html", candidatos=candidatos, votacion=ultimaVotacion)


@bp.route("/Resultados")
@login_required
def resultados():
    usuario_alias = aliased(Usuario)
    votos_por_candidato = (
        db.session.query(usuario_alias.nombreUsuario, db.func.count(Usuario.voto))
        .join(usuario_alias, Usuario.voto == usuario_alias.idUsuario)
        .filter(Usuario.voto.isnot(None))
        .group_by(usuario_alias.nombreUsuario)
        .all()
    )
    votacion = Votacion.query.order_by(asc(Votacion.idVotacion)).first()
    
    ultimaVotacion = Votacion.query.first()
    anio = ultimaVotacion.fechaInicioVotacion.year
    # ////////////////////

    votos = dict(votos_por_candidato)

    # Luego, puedes seguir con el mismo código que proporcionaste para generar el gráfico de torta
    nombres = list(votos.keys())
    valores = list(votos.values())

    imagen_base64 = getGrafico(nombres=nombres, valores=valores, anio=anio)
    # ////////////////////

    return render_template(
        "resultados-votacion.html",
        votacion=ultimaVotacion,
        graficoVotos=imagen_base64,
    )


def getGrafico(valores, nombres, anio):
    plt.figure(figsize=(8, 6), facecolor="none")
    plt.pie(valores, labels=nombres, autopct="%1.1f%%", colors=plt.cm.tab20.colors)
    # plt.title(f"Resultado de las votaciones {anio}")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Convertir el gráfico a formato base64 para mostrarlo en HTML
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return imagen_base64
