from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'general.login'
    
    @login_manager.user_loader
    def load_user(idUsuario):
        from app.models.Usuario import Usuario
        usuario = Usuario.query.get(int(idUsuario))
        return usuario


    from app.routes import usuario_route, general_route, administrador_route, votaciones_route
    
    app.register_blueprint(usuario_route.bp)
    app.register_blueprint(general_route.bp)
    app.register_blueprint(administrador_route.bp)
    app.register_blueprint(votaciones_route.bp)
    return app