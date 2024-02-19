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
import pytz, os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app import db
from app.routes.usuario_routes import send_mail
from app.routes.usuario_routes import get_graphic
from sqlalchemy.orm import aliased


bp = Blueprint("votacion", __name__)


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

        rs = send_mail(
            asunto="Votaciones para representandes CGAO",
            contenido=contenido,
            destinatario=["cfmorales.diaz20@gmail.com"],
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

        print(rs)

        porcentaje = (votos / totalVotos) * 100
        votacion.idGanador = usuario
        votacion.cantVotosVotacion = votos
        votacion.totalVotosVotacion = totalVotos
        votacion.porcentajeVotosVotacion = porcentaje

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
        db.session.add(new_sancion)


def candidato_a_aprendiz():
    candidatos = Usuario.query.filter_by(idRol=2).all()

    for candidato in candidatos:
        candidato.idRol = 1


# ////////////////////////////////////
