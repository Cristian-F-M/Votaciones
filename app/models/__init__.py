
# El código importa la clase `Libro` del módulo `libro` en el paquete `app.models` y la clase `Author`
# del módulo `autor` en el mismo paquete. Esto permite que el código utilice las clases `Libro` y
# `Autor` en el módulo actual.

# Se escribe el import de los modelos app.models.{modelo} import {modelo}

# from app.models.book import Book
# from app.models.author import Author
from app.models.Estado import Estado
from app.models.Rol import Rol
from app.models.Sancion import Sancion
from app.models.TipoDocumento import TipoDocumento
from app.models.Usuario import Usuario
from app.models.Votacion import Votacion