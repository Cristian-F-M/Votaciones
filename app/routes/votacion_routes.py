from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.decorators.admin_required import admin_required
from flask_login import login_required, current_user
from sqlalchemy import not_, asc
from app.models.Votacion import Votacion
from app.models.Usuario import Usuario
from app.models.Estado import Estado
from app.models.Sancion import Sancion
from sqlalchemy import func
from datetime import datetime
import pytz, os, random, json
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app import db
from app.routes.usuario_routes import send_mail
from app.routes.usuario_routes import get_graphic
from sqlalchemy.orm import aliased


bp = Blueprint("votacion", __name__)


with open("config.json") as f:
    config = json.load(f)


@bp.route("/add/votes", methods=["POST"])
@admin_required
def add():
    if request.method == "POST":
        correos = (
            Usuario.query.filter(Usuario.correoUsuario.isnot(None))
            .with_entities(Usuario.correoUsuario)
            .all()
        )

        fechaInicio = datetime.now(pytz.utc)
        fechaFin = request.form["fechaFinVotacion"]

        new_votacion = Votacion(
            fechaInicioVotacion=fechaInicio,
            fechaFinVotacion=fechaFin,
        )

        db.session.add(new_votacion)
        db.session.query(Usuario).update({Usuario.idVoto: None})
        db.session.commit()

        ultimaVotacion = Votacion.query.order_by(asc(Votacion.idVotacion)).first()

        contenido = render_template("componentes/correoInicioVotaciones.html")

        if config["correosInicioVotacion"]:
            rs = send_mail(
                asunto="Votaciones para representandes CGAO",
                contenido=contenido,
                destinatario=correos,
                finalMensaje="la información a los aprendices",
                tipoContenido="html",
            )

        msg = ""
        if rs["rs"] == 200:
            msg = ", se ha enviado la información a los aprendices."

        flash(["informacion", "Votacion Iniciada" + msg], "session")
        return redirect(url_for("administrador.view_votes"))


@bp.route("/Votes/Finish/<int:votacion>", methods=["POST"])
@admin_required
def finish_vote(votacion):

    if config["correosSancionesVotacion"]:
        añadir_sancion()

    usuario_alias = aliased(Usuario)
    votos = dict(
        (
            db.session.query(usuario_alias.nombreUsuario, db.func.count(Usuario.idVoto))
            .join(usuario_alias, Usuario.idVoto == usuario_alias.idUsuario)
            .filter(Usuario.idVoto.isnot(None))
            .group_by(usuario_alias.nombreUsuario)
            .all()
        )
    )

    grafico = get_graphic(anio=2024, votos=votos)

    candidato_a_aprendiz()

    rs = (
        db.session.query(Usuario.idVoto, func.count())
        .filter(Usuario.idVoto.isnot(None))
        .group_by(Usuario.idVoto)
        .order_by(func.count().desc())
        .first()
    )

    votacion = Votacion.query.get_or_404(votacion)

    totalVotos = (
        db.session.query(func.count(Usuario.idVoto))
        .filter(Usuario.idVoto.isnot(None))
        .scalar()
    )

    votacion.idEstado = 3

    if rs:
        usuario, votos = rs

        porcentaje = (votos / totalVotos) * 100
        votacion.idGanador = usuario
        votacion.cantVotosVotacion = votos
        votacion.totalVotosVotacion = totalVotos
        votacion.porcentajeVotosVotacion = porcentaje

    correos = (
        Usuario.query.filter(Usuario.correoUsuario.isnot(None))
        .with_entities(Usuario.correoUsuario)
        .all()
    )
    if config["correosFinVotacion"]:
        enviar_corre_finalizar(correos)

    db.session.commit()

    flash(
        ["informacion", "La votacion se ha finalizado, ya puedes ver el ganador"],
        "session",
    )

    return redirect(url_for("administrador.view_votes"))


@bp.route("/Votes/Delete/<int:votacion>", methods=["POST"])
@admin_required
def delete_vote(votacion):
    votacion = Votacion.query.get_or_404(votacion)

    db.session.delete(votacion)
    db.session.commit()

    flash(
        ["informacion", "La votacion se ha eliminado"],
        "session",
    )

    return redirect(url_for("administrador.view_votes"))


# ////////////////////////////////////


def añadir_sancion():
    usuariosSinVoto = Usuario.query.filter_by(idVoto=None)

    for usuario in usuariosSinVoto:
        new_sancion = Sancion(
            idUsuario=usuario.idUsuario,
            motivoSancion="No participar en las votaciones de representantes",
        )
        if not usuario.correoUsuario is None:
            sancion = generar_sancion()
            contenido = f"""La votaciones han finalizado y tu no votaste, lastimosamente tenemos que aplicarte una sancion aleatoria. La sanción que tienes que cumplir es: "{sancion}" """
            rs = send_mail(
                asunto="Votaciones para representandes CGAO",
                contenido=contenido,
                destinatario=usuario.correoUsuario,
                finalMensaje="la información a los aprendices",
            )

        db.session.add(new_sancion)


def candidato_a_aprendiz():
    candidatos = Usuario.query.filter_by(idRol=2).all()

    for candidato in candidatos:
        candidato.idRol = 1


# ////////////////////////////////////


def generar_sancion():
    sanciones = [
        "Hacer el aseo de tu ambiente 2 días.",
        "Hacer el aseo de una determinada zona del centro,",
        "Traer un árbol para plantar.",
        "Colaborar con biestar al aprendiz en la organización de 1 actividad",
        "Participar activamente en las proximas 2 actividades de bienestar al aprendiz.",
        "Realizar un trabajo más extenso que sus compañero proporcionado por su instructor",
        "Realizar una exposición sobre la importancia de la democracia en ingles (la debe exponer frente al instructor de ingles y a sus compañeros).",
    ]
    rm = random.randint(a=0, b=len(sanciones) - 1)
    return sanciones[rm]


def enviar_corre_finalizar(correos):
    for correo in correos:
        contenido = render_template("componentes/correoFinalVotacion.html")

        rs = send_mail(
            asunto="Votaciones para representandes CGAO",
            contenido=contenido,
            destinatario=correo,
            finalMensaje="la información a los aprendices",
            tipoContenido="html",
        )
