from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.Votacion import Votacion
from app.models.Usuario import Usuario
from app.models.Estado import Estado
from sqlalchemy import func
from datetime import datetime
import pytz, os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


from app import db


bp = Blueprint("votaciones", __name__)


@bp.route("/Votaciones/crear", methods=["POST"])
def crear():
    if not isAdmin():
        return redirect(url_for("general.inicio"))

    if request.method == "POST":

        # correos = (
        #     Usuario.query.filter(Usuario.correoUsuario.isnot(None))
        #     .with_entities(Usuario.correoUsuario)
        #     .all()
        # )
        estado = Estado.query.first()

        fechaInicio = datetime.now(pytz.utc)
        fechaFin = request.form["fechaInicioVotacion"]

        new_votacion = Votacion(
            fechaInicioVotacion=fechaInicio,
            fechaFinVotacion=fechaFin,
            estadoVotacion=estado.idEstado,
        )

        db.session.add(new_votacion)
        db.session.query(Usuario).update({Usuario.voto: None})
        db.session.commit()

        correos = ["cfmorales.diaz@gmail.com"]
        enviarCorreos(correos)

        flash(["informacion", "Votacion Iniciada"], "session")
    return redirect(url_for("administrador.votaciones"))


@bp.route("/Votaciones/Finalizar/<int:idVotacion>", methods=["POST"])
def finalizarVotacion(idVotacion):
    rs = (
        db.session.query(Usuario.voto, func.count())
        .filter(Usuario.voto.isnot(None))
        .group_by(Usuario.voto)
        .order_by(func.count().desc())
        .first()
    )

    if rs:
        usuario, votos = rs
        votacion = Votacion.query.get_or_404(idVotacion)

        totalVotos = (
            db.session.query(func.count(Usuario.voto))
            .filter(Usuario.voto.isnot(None))
            .scalar()
        )

        porcentaje = (votos / totalVotos) * 100

        votacion.estadoVotacion = 5
        votacion.ganadorVotacion = usuario
        votacion.cantVotosVotacion = votos
        votacion.porcentajeVotosVotacion = porcentaje
        votacion.totalVotosVotacion = totalVotos
        db.session.commit()

        flash(
            ["informacion", "La votacion se ha finalizado, ya puedes ver el ganador"],
            "session",
        )
    return redirect(url_for("administrador.votaciones"))


@bp.route("/Votaciones/eliminar/<int:idVotacion>", methods=["POST"])
def eliminarVotacion(idVotacion):
    votacion = Votacion.query.get_or_404(idVotacion)

    db.session.delete(votacion)
    db.session.commit()

    flash(
        ["informacion", "La votacion se ha eliminado"],
        "session",
    )

    return redirect(url_for("administrador.votaciones"))


def isAdmin():
    rs = current_user.rolUsuario.idRol == 36 or current_user.rolUsuario.idRol == 35
    return rs


def enviarCorreos(correos):
    load_dotenv()

    smtp_user = os.getenv("smtp_user")
    smtp_password = os.getenv("smtp_password")
    smtp_host = os.getenv("smtp_host")
    smtp_port = int(os.getenv("smtp_port"))
    smtp_name = os.getenv("smtp_name")

    contenido = render_template("componentes/correoInicioVotaciones.html")

    asunto = "Inicio de las Votaciones"
    mensaje = MIMEMultipart()
    mensaje["From"] = smtp_name
    mensaje["To"] = ", ".join(correos)
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(contenido, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
        servidor_smtp.starttls()
        servidor_smtp.login(smtp_user, smtp_password)
        servidor_smtp.send_message(mensaje)
