from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(idUsuario):
        from app.models.Usuario import Usuario

        usuario = Usuario.query.get(int(idUsuario))
        return usuario

    from app.routes import (
        usuario_routes,
        auth_routes,
        administrador_routes,
        votacion_routes,
        rol_routes,
        estado_routes,
        sancion_routes,
        tipoDocumento_routes
    )

    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(administrador_routes.bp)
    app.register_blueprint(votacion_routes.bp)
    app.register_blueprint(sancion_routes.bp)
    app.register_blueprint(rol_routes.bp)
    app.register_blueprint(estado_routes.bp)
    app.register_blueprint(tipoDocumento_routes.bp)
    return app
