from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('general.login'))

    # Importar las rutas que tengamos 
    # Se hace un register_blueprint con cada ruta    
    
    from app.routes import usuario_route, general_route
    
    app.register_blueprint(usuario_route.bp)
    app.register_blueprint(general_route.bp)
    return app