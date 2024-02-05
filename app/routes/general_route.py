from flask import Blueprint, render_template
from flask_login import login_required
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion
import plotly.graph_objs as go

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
    votos_por_candidato = (
        db.session.query(Usuario.voto, db.func.count(Usuario.voto))
        .group_by(Usuario.voto)
        .all()
    )

    print(votos_por_candidato)
    graph_json = generar_grafico_barras(votos_por_candidato)


    ultimaVotacion = Votacion.query.first()
    return render_template(
        "resultados-votacion.html", votacion=ultimaVotacion, rs=votos_por_candidato, graph_json=graph_json
    )


# Función para generar el gráfico de barras
def generar_grafico_barras(conteo_votos):
    # Separar los datos en dos listas: candidatos y cantidades de votos
    candidatos = [voto[0] for voto in conteo_votos]
    cant_votos = [voto[1] for voto in conteo_votos]

    # Crear el objeto de datos para el gráfico de barras
    data = [go.Bar(x=candidatos, y=cant_votos, marker=dict(color="rgb(26, 118, 255)"))]

    # Configurar el diseño del gráfico
    layout = go.Layout(
        title="Conteo de Votos por Candidato",
        xaxis=dict(title="Candidato"),
        yaxis=dict(title="Cantidad de Votos"),
    )

    # Crear la figura del gráfico
    fig = go.Figure(data=data, layout=layout)

    # Convertir la figura en un objeto JSON
    graph_json = fig.to_json()

    return graph_json
