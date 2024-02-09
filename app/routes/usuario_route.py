from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask_login import login_required, logout_user, login_user, current_user
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError
import bcrypt, random, re, os
from dotenv import load_dotenv
# El código anterior importa el módulo `smtplib`, que es un módulo integrado en Python para enviar
# correos electrónicos utilizando el Protocolo simple de transferencia de correo (SMTP).
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# from app.models.author import Author
# Estas líneas están importando los modelos `Usuario` y `TipoDocumento` desde el módulo `app.models`.
# Es probable que estos modelos estén definidos en archivos separados y se utilicen en el módulo
# actual para operaciones de bases de datos u otras funciones.
from app.models.Usuario import Usuario
from app.models.TipoDocumento import TipoDocumento
from app.models.Rol import Rol
from app.models.Votacion import Votacion
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
    session["usernameUsuario"] = usernameUsuario

    flash(["informacion", f"Bienvenido/a {usernameUsuario}"], "session")

    rs = current_user.rolUsuario.idRol == 36 or current_user.rolUsuario.idRol == 35

    if rs:
        return redirect(url_for("administrador.inicio_administrador"))

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

            print(ex.orig)
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
@login_required
def perfil():
    ultimaVotacion = Votacion.query.first()
    tiposDocumento = TipoDocumento.query.all()
    return render_template(
        "usuario-perfil.html", TiposDocumento=tiposDocumento, votacion=ultimaVotacion
    )


@bp.route("/Votar", methods=["POST"])
def votar():
    candidato = request.form["candidatoUsuario"]

    usuario = Usuario.query.get_or_404(current_user.idUsuario)
    usuario.voto = candidato

    db.session.commit()

    flash(["informacion", "Voto registrado con exito"], "session")
    return redirect(url_for("administrador.inicio_administrador"))


@bp.route("/editar-perfil/<int:usuario>", methods=["POST"])
@login_required
def editar_perfil(usuario):
    usuario = Usuario.query.get_or_404(usuario)

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
            eliminarFoto(current_user.idUsuario)
            usuario.fotoUsuario = nameFotoUsuario(usuario, foto.filename)
            guardarFotoUsuario(foto, usuario)

    if "contraseniaOldUsuario" in request.form and "contraseniaUsuario" in request.form:
        contrasenia_old = request.form["contraseniaOldUsuario"]
        contrasenia_nueva = request.form["contraseniaUsuario"]
        if contrasenia_old and contrasenia_nueva:
            if bcrypt.checkpw(
                contrasenia_old.encode("utf-8"),
                usuario.contraseniaUsuario.encode("utf-8"),
            ):
                usuario.contraseniaUsuario = bcrypt.hashpw(
                    contrasenia_nueva.encode("utf-8"), bcrypt.gensalt()
                )
            else:
                flash(["error", "Las contraseñas no coinciden"], "session")
                return redirect(
                    url_for("usuario.editar_perfil", usuario=usuario.idUsuario)
                )
        else:
            flash(
                ["error", "Se requieren la contraseña anterior y la nueva"], "session"
            )
            return redirect(url_for("usuario.editar_perfil", usuario=usuario.idUsuario))

    db.session.commit()

    flash(["informacion", "Perfil actualizado"], "session")
    return redirect(url_for("administrador.inicio_administrador"))


@bp.route("/Enviar-sugerencias", methods=["POST"])
def enviarSugerencia():

    load_dotenv()

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

    servidor_smtp = smtplib.SMTP(os.getenv("smtp_host"), os.getenv("smtp_port"))
    servidor_smtp.starttls()
    servidor_smtp.login(os.getenv("smtp_user"), os.getenv("smtp_password"))

    msg = MIMEMultipart()
    msg["From"] = os.getenv("smtp_user")
    msg["To"] = os.getenv("smtp_user_to")
    msg["Subject"] = "Sugerencias"
    msg.attach(MIMEText(mensaje))

    servidor_smtp.sendmail(
        os.getenv("smtp_user_to"), os.getenv("smtp_user_to"), msg.as_string()
    )
    servidor_smtp.quit()

    return "Se ha enviado tu sugerencia"


def validarContraseña(contrasenia):
    patron = re.compile(r"^.{8,}$")
    return True if patron.match(contrasenia) else False


def columnaDuplicada(exOrigin):
    return str(exOrigin).split("key")[-1].split(".")[-1].split("'")[0]


def getCodigo(tamanio):
    mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "1234567890"
    opciones = [mayus, digitos]

    codigo = ""
    for _ in range(tamanio):
        opcion = random.choice(opciones)
        codigo += random.choice(opcion)

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


def guardarFotoUsuario(file, usuario):
    from run import app

    filename = file.filename

    destination_folder = os.path.join(app.root_path, "static", "images")

    file.save(
        os.path.join(
            destination_folder, nameFotoUsuario(usuario=usuario, filename=filename)
        )
    )


def nameFotoUsuario(usuario, filename):
    formato = os.path.splitext(filename)[1]
    name = f"perfil_{usuario.nombreUsuario}{formato}"
    return name


def eliminarFoto(idUsuario):
    from run import app

    fotoUsuario = Usuario.query.get_or_404(idUsuario).fotoUsuario

    ruta_imagen = os.path.join(app.root_path, "static", "images", fotoUsuario)

    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
