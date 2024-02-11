from flask import Blueprint

bp = Blueprint('main', __name__)



# La línea `from app.routes import book_routes, Author_routes` está importando los módulos
# `book_routes` y `author_routes` del paquete `app.routes`. Esto permite que las rutas definidas en
# esos módulos se utilicen en el módulo actual.

#Importar las rutas
# from app.routes import book_routes, author_routes
from app.routes import usuario_routes
from app.routes import auth_routes
from app.routes import administrador_routes
from app.routes import votacion_route