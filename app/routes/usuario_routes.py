from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask import Blueprint, render_template
from sqlalchemy.orm import aliased
from sqlalchemy import not_, asc
import random, os, bcrypt
import smtplib
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion
from app import db

bp = Blueprint("usuario", __name__)


@bp.route("/Profile", methods=["GET"])
@login_required
def view_profile():
    votacion = Votacion.query.first()
    return render_template("usuario/profile-user.html", votacion=votacion)


@bp.route("/Home")
@login_required
def view_home():
    votacion = Votacion.query.first()
    return render_template("usuario/index.html", votacion=votacion)


@bp.route("/Vote")
@login_required
def view_vote():
    ultimaVotacion = Votacion.query.first()
    candidatos = Usuario.query.filter_by(idRol=34).all()
    return render_template(
        "usuario/votar.html", candidatos=candidatos, votacion=ultimaVotacion
    )


@bp.route("/Results")
@login_required
def view_results():
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

    anio = ""
    ultimaVotacion = Votacion.query.order_by(asc(Votacion.idVotacion)).first()
    if ultimaVotacion:
        anio = ultimaVotacion.fechaInicioVotacion.year

    grafico = get_graphic(votos, anio=anio)

    return render_template(
        "usuario/results-votes.html", graficoVotos=grafico, votacion=ultimaVotacion
    )


@bp.route("/save-vote", methods=["POST"])
def vote():
    candidato = request.form["candidatoUsuario"]
    usuario = Usuario.query.get_or_404(current_user.idUsuario)
    usuario.voto = candidato
    db.session.commit()
    flash(["informacion", "Voto registrado con exito"], "session")
    return redirect(url_for("usuario.inicio"))


@bp.route("/edit-profile/", methods=["POST"])
@login_required
def edit_profile():
    usuario = Usuario.query.get_or_404(current_user.idUsuario)
    usuario.nombreUsuario = request.form.get("nombreUsuario", usuario.nombreUsuario)
    usuario.apellidoUsuario = request.form.get(
        "apellidoUsuario", usuario.apellidoUsuario
    )
    usuario.documentoUsuario = request.form.get(
        "documentoUsuario", usuario.documentoUsuario
    )
    usuario.correoUsuario = request.form.get("correoUsuario", usuario.correoUsuario)
    usuario.telefonoUsuario = request.form.get(
        "telefonoUsuario", usuario.telefonoUsuario
    )
    usuario.descripcionUsuario = request.form.get(
        "descripcionUsuario", usuario.descripcionUsuario
    )

    if "fotoUsuario" in request.files:
        foto = request.files["fotoUsuario"]
        if foto.filename != "":
            delete_user_photo(current_user.idUsuario)
            usuario.fotoUsuario = name_user_photo(usuario, foto.filename)
            save_user_photo(foto, usuario)

    if "contraseniaOldUsuario" in request.form and "contraseniaUsuario" in request.form:
        c_old = request.form["contraseniaOldUsuario"]
        c_nueva = request.form["contraseniaUsuario"]

        if len(c_nueva) < 8:
            error = [
                "contraseniaUsuario",
                "La contraseña debe tener mínimo 8 caracteres",
            ]
            flash(error, "session")
            return redirect(url_for("usuario.view_profile"))

        if c_old and c_nueva:
            if not bcrypt.checkpw(c_old.encode("utf-8"), usuario.contraseniaUsuario):
                flash(["error", "Algunos datos son invalidos"], "session")
                return redirect(url_for("usuario.view_profile"))

            usuario.contraseniaUsuario = bcrypt.hashpw(
                c_nueva.encode("utf-8"), bcrypt.gensalt()
            )

    db.session.commit()
    flash(["informacion", "Perfil actualizado"], "session")
    return redirect(url_for("administrador.view_home"))


@bp.route("/Search/Apprentice", methods=["POST"])
def search_apprentice():
    data = request.json
    documentoUsuario = data["documentoUsuario"]

    usuario = (
        Usuario.query.filter_by(documentoUsuario=documentoUsuario)
        .filter(~Usuario.idRol.in_([3, 4]))
        .first()
    )

    if not usuario:
        return {"rs": 404}

    descripcionUsuarioV = (
        True
        if usuario.descripcionUsuario or usuario.descripcionUsuario != ""
        else False
    )
    fotoUsuarioV = True if usuario.fotoUsuario or usuario.fotoUsuario != "" else False
    estadoUsuarioV = True if usuario.idEstado == 1 else False

    valido = True if descripcionUsuarioV and fotoUsuarioV and estadoUsuarioV else False

    usuario = {
        "idUsuario": usuario.idUsuario,
        "nombreUsuario": usuario.nombreUsuario,
        "usuarioValido": valido,
        "rolUsuario": usuario.rolUsuario.descripcionRol,
        "fotoUsuario": fotoUsuarioV,
        "descripcionUsuario": descripcionUsuarioV,
        "estadoUsuarioV": estadoUsuarioV,
        "estadoUsuario": usuario.estadoUsuario.descripcionEstado,
    }
    return {"rs": 304, "usuario": usuario}


@bp.route("/search/user", methods=["POST"])
def search_user():

    data = request.json
    documentoUsuario = data["documentoUsuario"]

    usuario = Usuario.query.filter_by(documentoUsuario=documentoUsuario).first()

    if not usuario:
        return {"rs": 404}

    rs = {"rs": 200, "idUsuario": usuario.idUsuario}

    return rs


@bp.route("/add/Candidate/<int:usuario>", methods=["POST"])
def add_candidate(usuario):
    usuario = Usuario.query.get_or_404(usuario)
    usuario.idRol = 2
    db.session.commit()

    flash(["informacion", "El aprendiz ahora es candidato"], "session")
    return redirect(url_for("administrador.view_home"))


@bp.route("/Send-suggestion", methods=["POST"])
def send_suggestion():

    data = request.json
    correo = data["correo"]
    mensaje = data["mensaje"]
    nombre = data["nombre"]

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mensaje += f"""
    
    Envía:
    {correo}
    {nombre}
    {fecha}"""
    try:
        send_mail(
            asunto="Sugerencias",
            destinatario="cfmorales.diaz20@gmail.com",
            finalMensaje="tu sugerencia",
            contenido=mensaje,
        )
    except Exception:
        return "500"

    return "200"


@bp.route("/edit/user/<int:usuario>", methods=["POST"])
def edit_user(usuario):
    usuario = Usuario.query.get_or_404(usuario)

    nombreUsuario = request.form["nombreUsuario"]
    apellidoUsuario = request.form["apellidoUsuario"]
    idTipoDocumento = request.form["tipoDocumentoUsuario"]
    usuario.nombreUsuario = nombreUsuario
    usuario.apellidoUsuario = apellidoUsuario
    usuario.idTipoDocumento = idTipoDocumento
    db.session.commit()

    flash(["informacion", "Se edito el usuario"], "session")
    return redirect(url_for("administrador.view_usuario"))

@bp.route("/Restablecer/Contraseña/<int:usuario>", methods=["POST"])
def reset_password(usuario):
    usuario = Usuario.query.get_or_404(usuario)
    contraseniaUsuario = request.form['contraseniaUsuario'].encode('utf-8')
    usuario.contraseniaUsuario = bcrypt.hashpw(password=contraseniaUsuario, salt=bcrypt.gensalt())
    usuario.codigoUsuario = None
    
    db.session.commit()
    flash(['informacion', 'Tu contraseña se cambió. Ya puedes iniciar sesión'], 'session')
    return redirect(url_for('auth.view_login'))
    
# //////////////////////////////////////////////
# Funciones


def save_user_photo(file, usuario):
    from run import app

    filename = file.filename
    destination_folder = os.path.join(app.root_path, "static", "images")
    file.save(
        os.path.join(
            destination_folder, name_user_photo(usuario=usuario, filename=filename)
        )
    )


def name_user_photo(usuario, filename):
    formato = os.path.splitext(filename)[1]
    name = f"perfil_{usuario.nombreUsuario}{formato}"
    return name


def delete_user_photo(idUsuario):
    from run import app

    fotoUsuario = Usuario.query.get_or_404(idUsuario).fotoUsuario
    ruta_imagen = os.path.join(app.root_path, "static", "images", fotoUsuario)
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)


def send_mail(asunto, destinatario, contenido, finalMensaje, tipoContenido="plain"):
    load_dotenv()

    smtp_user = os.getenv("smtp_user")
    smtp_password = os.getenv("smtp_password")
    smtp_host = os.getenv("smtp_host")
    smtp_port = os.getenv("smtp_port")
    smtp_name = os.getenv("smtp_name")

    mensaje = MIMEMultipart()

    mensaje["From"] = smtp_name
    if isinstance(destinatario, list):
        mensaje["To"] = ", ".join(destinatario)
    else:
        mensaje["To"] = destinatario

    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(contenido, tipoContenido))
    
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
            servidor_smtp.starttls()
            servidor_smtp.login(smtp_user, smtp_password)
            servidor_smtp.sendmail(smtp_user, destinatario, mensaje.as_string())

            return {
                "rs": 200,
                "msj": f"Se ha enviado {finalMensaje}",
            }
    except Exception as ex:
        return {
            "rs": 500,
            "msj": "Ocurrio un error al procesar la peticion, intentalo más tarde"
            + str(ex),
        }


def get_graphic(votos, anio):
    nombres = list(votos.keys())
    valores = list(votos.values())

    plt.figure(figsize=(8, 6), facecolor="none")
    plt.pie(valores, labels=nombres, autopct="%1.1f%%", colors=plt.cm.tab20.colors)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return imagen_base64


def getCodigo(tamanio):
    mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "1234567890"
    opciones = [mayus, digitos]

    codigo = ""
    for _ in range(tamanio):
        opcion = random.choice(opciones)
        codigo += random.choice(opcion)

    return codigo


# //////////////////////////////////////////////
