from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, LoginManager, logout_user, login_user
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError
import bcrypt
import re, os, random
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# from app.models.author import Author
# Estas líneas están importando los modelos `Usuario` y `TipoDocumento` desde el módulo `app.models`.
# Es probable que estos modelos estén definidos en archivos separados y se utilicen en el módulo
# actual para operaciones de bases de datos u otras funciones.
from app.models.Usuario import Usuario
from app.models.TipoDocumento import TipoDocumento
from app.models.Rol import Rol
from app.models.Estado import Estado

# La línea `from app import db` está importando el objeto `db` desde el módulo `app`. Este objeto es
# una instancia de la clase SQLAlchemy `SQLAlchemy`, que se utiliza para interactuar con la base de
# datos en la aplicación Flask. Proporciona métodos y atributos para administrar conexiones de bases
# de datos, ejecutar consultas y realizar otras operaciones relacionadas con bases de datos.
from app import db


bp = Blueprint("usuario", __name__)


@bp.route("/restablecer-contraseña")
def restablecer_contrasenia():
    return render_template("auth/restablecer_contrasenia.html")


@bp.route("/verificar-usuario")
def verificar_usuario():
    return render_template("auth/verificar-usuario.html")


@bp.route("/Iniciar-sesion", methods=["POST"])
def iniciar_sesion():
    tipoDocumentoUsuario = request.form["tipoDocumentoUsuario"]
    documentoUsuario = request.form["documentoUsuario"]
    contraseniaUsuario = request.form["contraseniaUsuario"]

    usuario = Usuario.query.filter_by(
        idTipoDocumento=tipoDocumentoUsuario, documentoUsuario=documentoUsuario
    ).first()

    if not usuario:
        flash(
            ["error", "No encontramos tu usuario, intenta registrarte primero"],
            "session",
        )
        return redirect(url_for("general.login"))

    if not bcrypt.checkpw(
        hashed_password=usuario.contraseniaUsuario,
        password=contraseniaUsuario.encode("utf-8"),
    ):
        flash(
            ["error", "Las credenciales no coinciden con nuestro registros"], "session"
        )
        return redirect(url_for("general.login"))

    login_user(usuario)

    usernameUsuario = getUsername(usuario)

    session["idUsuario"] = usuario.idUsuario
    session["apellidoUsuario"] = usuario.apellidoUsuario
    session["usernameUsuario"] = usernameUsuario
    session["tipoDocumentoUsuario"] = usuario.tipoDocumentoUsuario.to_dict()
    session["documentoUsuario"] = usuario.documentoUsuario
    session["correoUsuario"] = usuario.correoUsuario
    session["telefonoUsuario"] = usuario.telefonoUsuario
    session["nombreUsuario"] = usuario.nombreUsuario
    session["rolUsuario"] = usuario.rolUsuario.to_dict()
    session["descripcionUsuario"] = usuario.descripcionUsuario
    session["fotoUsuario"] = usuario.fotoUsuario
    session["votoUsuario"] = usuario.votoUsuario

    flash(["informacion", f"Bienvenido/a {usernameUsuario}"], "session")

    rs = usuario.rolUsuario.idRol == 36 or usuario.rolUsuario.idRol == 35

    if rs:
        return redirect(url_for('administrador.inicio_administrador'))
    
    return redirect(url_for("general.inicio"))


@bp.route("/Iniciar-sesion", methods=["GET"])
@login_required
def cerrarSesion():
    logout_user()
    flash(["informacion", "Tu sesión ha sido cerrada"], "session")
    return redirect(url_for("general.login"))


@bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombreUsuario = request.form["nombreUsuario"]  #
        apellidoUsuario = request.form["apellidoUsuario"]  #
        tipoDocumentoUsuario = request.form["tipoDocumentoUsuario"]  #
        documentoUsuario = request.form["documentoUsuario"]  #
        correoUsuario = request.form["correoUsuario"]  #
        telefonoUsuario = request.form["telefonoUsuario"]  #
        contraseniaUsuario = request.form["contraseniaUsuario"]  #
        contraseniaUsuario_confirm = request.form["contraseniaUsuario_confirm"]

        try:
            tipoDocumentoUsuario = int(tipoDocumentoUsuario)
        except Exception:
            print("Error al parsear el tipoDocumento")

        usuario = {
            "nombreUsuario": nombreUsuario,
            "apellidoUsuario": apellidoUsuario,
            "tipoDocumentoUsuario": tipoDocumentoUsuario,
            "documentoUsuario": documentoUsuario,
            "correoUsuario": correoUsuario,
            "telefonoUsuario": telefonoUsuario,
        }

        rol = Rol.query.first()
        estado = Estado.query.first()

        try:
            new_usuario = Usuario(
                nombreUsuario=nombreUsuario,
                apellidoUsuario=apellidoUsuario,
                idTipoDocumento=tipoDocumentoUsuario,
                documentoUsuario=documentoUsuario,
                correoUsuario=correoUsuario,
                telefonoUsuario=telefonoUsuario,
                idRol=rol.idRol,
                estadoUsuario=estado.idEstado,
                contraseniaUsuario=bcrypt.hashpw(
                    contraseniaUsuario.encode("utf-8"), bcrypt.gensalt()
                ),
            )
            db.session.add(new_usuario)
            db.session.commit()
        except IntegrityError as ex:
            db.session.rollback()
            columna = columnaDuplicada(ex.orig)
            inputName = columna.split("U")[0]
            error = f"El {inputName} no está disponible"

            flash(usuario, "usuarioOld")
            error = [columna, error]
            flash(error, "session")
            return redirect(url_for("general.register"))

        if contraseniaUsuario != contraseniaUsuario_confirm:
            flash(usuario, "usuarioOld")
            return redirect(url_for("general.register"))

        if not validarContraseña(contraseniaUsuario):
            flash(usuario, "usuarioOld")
            error = [
                "contraseniaUsuario",
                "La contraseña debe tener mínimo 8 caracteres",
            ]
            flash(error, "session")
            return redirect(url_for("general.register"))

        flash(["informacion", "Cuenta creada con exito"], "session")
        return redirect(url_for("general.login"))

    return redirect(url_for("general.register"))

@bp.route("/verificar", methods=["GET", "POST"])
def verificarCorreo():
    correo = request.json["correo"]
    enviar_correo(correo)
    return ""

@bp.route("/perfil", methods=["GET"])
def perfil():
    return render_template('usuario-perfil.html')



def validarContraseña(contrasenia):
    patron = re.compile(r"^.{8,}$")
    return True if patron.match(contrasenia) else False


def columnaDuplicada(exOrigin):
    return str(exOrigin).split("key")[-1].split(".")[-1].split("'")[0]


def getCodigo(tamanio):
    mayus = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    digitos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    a = [mayus, digitos]
    codigo = ""

    for i in range(tamanio):
        nList = random.randint(0, len(a) - 1)
        list = a[nList]
        nCaracter = random.randint(0, len(list) - 1)
        caracter = str(list[nCaracter])
        codigo += caracter
    return codigo


def enviar_correo(correo):
    load_dotenv()

    smtp_user = os.getenv("smtp_user")
    smtp_password = os.getenv("smtp_password")
    smtp_host = os.getenv("smtp_host")
    smtp_port = os.getenv("smtp_port")
    smtp_name = os.getenv("smtp_name")

    asunto = "Código de verificación del correo"
    destinatario = correo
    contenido = getCodigo(8)
    mensaje = MIMEMultipart()

    mensaje.attach(MIMEText(contenido, "plain"))

    mensaje["From"] = smtp_name
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    with smtplib.SMTP(smtp_host, smtp_port) as servidor_smtp:
        servidor_smtp.starttls()
        servidor_smtp.login(smtp_user, smtp_password)
        servidor_smtp.sendmail(smtp_user, destinatario, mensaje.as_string())


def getUsername(usuario):
    nombre = usuario.nombreUsuario.split(" ")[0]
    apellido = usuario.apellidoUsuario.split(" ")[0]
    return nombre + " " + apellido
