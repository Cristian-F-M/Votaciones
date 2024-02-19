from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError
import bcrypt, random
from app.models.Usuario import Usuario
from app.models.TipoDocumento import TipoDocumento
from app.routes.usuario_routes import send_mail

bp = Blueprint("auth", __name__)


@bp.route("/", methods=["GET"])
def view_login():
    tiposDocumento = TipoDocumento.query.all()
    return render_template("auth/login.html", tiposDocumento=tiposDocumento)


@bp.route("/Register", methods=["GET"])
def view_register():
    tiposDocumento = TipoDocumento.query.all()
    return render_template("auth/register.html", tiposDocumento=tiposDocumento)


@bp.route("/verificar-usuario")
def view_verify_user():
    return render_template("auth/verificar-usuario.html")


@bp.route("/Verificar-codigo/<int:u>/<string:c>", methods=["GET"])
def view_verificar_codigo(u, c):
    return render_template("auth/verificar-codigo.html", idUsuario=u, correoOculto=c)


@bp.route("/registrar", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombreUsuario = request.form["nombreUsuario"]  #
        apellidoUsuario = request.form["apellidoUsuario"]  #
        tipoDocumentoUsuario = request.form["tipoDocumentoUsuario"]  #
        documentoUsuario = request.form["documentoUsuario"]  #
        correoUsuario = request.form["correoUsuario"]  #
        telefonoUsuario = request.form["telefonoUsuario"]  #
        contraseniaUsuario = request.form["contraseniaUsuario"]  #
        contraseniaUsuario_confirm = request.form["contraseniaUsuario_confirm"]

        usuario = {
            "nombreUsuario": nombreUsuario,
            "apellidoUsuario": apellidoUsuario,
            "tipoDocumentoUsuario": tipoDocumentoUsuario,
            "documentoUsuario": documentoUsuario,
            "correoUsuario": correoUsuario,
            "telefonoUsuario": telefonoUsuario,
        }

        try:
            new_usuario = Usuario(
                nombreUsuario=nombreUsuario,
                apellidoUsuario=apellidoUsuario,
                idTipoDocumento=tipoDocumentoUsuario,
                documentoUsuario=documentoUsuario,
                correoUsuario=correoUsuario,
                telefonoUsuario=telefonoUsuario,
                contraseniaUsuario=bcrypt.hashpw(
                    contraseniaUsuario.encode("utf-8"), bcrypt.gensalt()
                ),
            )
            
            if len(contraseniaUsuario) < 8:
                flash(usuario, "usuarioOld")
                error = [
                    "contraseniaUsuario",
                    "La contraseña debe tener mínimo 8 caracteres",
                ]
                flash(error, "session")
                return redirect(url_for("auth.view_register"))

            if contraseniaUsuario != contraseniaUsuario_confirm:
                flash(usuario, "usuarioOld")
                return redirect(url_for("auth.view_register"))
                
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
            return redirect(url_for("auth.view_register"))

        

        flash(["informacion", "Cuenta creada con exito"], "session")
        return redirect(url_for("auth.view_login"))

    return redirect(url_for("auth.view_register"))


@bp.route("/Login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        tipoDocumentoUsuario = request.form["tipoDocumentoUsuario"]
        documentoUsuario = request.form["documentoUsuario"]
        contraseniaUsuario = request.form["contraseniaUsuario"]

        usuario = Usuario.query.filter_by(
            idTipoDocumento=tipoDocumentoUsuario, documentoUsuario=documentoUsuario
        ).first()

        if usuario:
            if bcrypt.checkpw(
                hashed_password=usuario.contraseniaUsuario,
                password=contraseniaUsuario.encode("utf-8"),
            ):
                login_user(usuario)

                flash(
                    ["informacion", f"Bienvenido/a {current_user.nombreUsuario}"],
                    "session",
                )

                rs = (
                    current_user.rolUsuario.idRol == 3
                    or current_user.rolUsuario.idRol == 4
                )

                if rs:
                    return redirect(url_for("administrador.view_home"))
                return redirect(url_for("usuario.view_home"))

        flash(["error", "Las credenciales no coinciden"], "session")
        return redirect(url_for("auth.view_login"))

    return redirect(url_for("auth.view_login"))


@bp.route("/Logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash(["informacion", "Tu sesión ha sido cerrada"], "session")
    return redirect(url_for("auth.login"))


@bp.route("/send/code", methods=["POST"])
def send_code():
    correoUsuario = request.form["correoUsuario"]

    usuario = Usuario.query.filter_by(correoUsuario=correoUsuario).first()

    if not usuario:
        flash(["error", "No encontramos tu correo, revisalo."], "session")
        return redirect(url_for("auth.view_verify_user"))

    codigo = gen_codigo(8)
    usuario.codigoUsuario = codigo

    db.session.commit()
    correoCodigo = render_template("componentes/correoCodigo.html", codigo=codigo)
    rs = send_mail(
        asunto="Código de verificación de usuario",
        contenido=correoCodigo,
        destinatario=correoUsuario,
        tipoContenido="html",
        finalMensaje="el código a tu correo",
    )

    if rs["rs"] == 500:
        flash(["error", f"{rs.msj}"], "session")
        return redirect(url_for("auth.view_verify_user"))

    return redirect(url_for('auth.view_verificar_codigo', u=usuario.idUsuario, c=get_correo_oculto(usuario.correoUsuario)))
    return render_template(
        "auth/verificar-codigo.html",
        usuario=usuario,
        correoOculto=get_correo_oculto(usuario.correoUsuario),
    )


@bp.route("/Verificar/Codigo/<int:usuario>", methods=["POST"])
def verificar_codigo(usuario):
    usuario = Usuario.query.get_or_404(usuario)
    codigoUsuario = request.form["codigoUsuario"]

    if not codigoUsuario == usuario.codigoUsuario:
        flash(
            ["error", "El código no coincide, verificalo y vuelve a intentarlo"],
            "session",
        )
        return render_template("auth/verificar-codigo.html", idUsuario=usuario.idUsuario)

    return render_template("auth/reset-password.html", usuario=usuario)


# //////////////////////////////////////////////
# Funciones


def columnaDuplicada(exOrigin):
    return str(exOrigin).split("key")[-1].split(".")[-1].split("'")[0]


def gen_codigo(tamanio):
    mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "1234567890"
    opciones = [mayus, digitos]

    codigo = ""
    for _ in range(tamanio):
        opcion = random.choice(opciones)
        codigo += random.choice(opcion)

    return codigo


def get_correo_oculto(correo):
    correoOculto = ""
    correoDividido = correo.split("@")
    tamanio = len(correoDividido[0])

    for i, letra in enumerate(correoDividido[0]):
        if i > int(tamanio / 2):
            caracter = "*" if (tamanio - i) >= 2 else letra
            correoOculto += caracter

    correoOculto += "@"
    correoOculto += correoDividido[1]

    return correoOculto


# //////////////////////////////////////////////
