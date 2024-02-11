from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError
import bcrypt, random
from app.models.Usuario import Usuario
from app.models.TipoDocumento import TipoDocumento

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


@bp.route("/Forgot-Password", methods=["GET"])
def view_forgot_password():
    tiposDocumento = TipoDocumento.query.all()
    return render_template("auth.register", tiposDocumento=tiposDocumento)


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


# //////////////////////////////////////////////
# Funciones


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


# //////////////////////////////////////////////
