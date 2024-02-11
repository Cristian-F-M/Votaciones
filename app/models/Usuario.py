from app import db
from flask_login import UserMixin


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    apellidoUsuario = db.Column(db.String(50), nullable=False)
    idTipoDocumento = db.Column(
        db.Integer, db.ForeignKey("tiposdocumento.idTipoDocumento"), nullable=False
    )
    tipoDocumentoUsuario = db.relationship("TipoDocumento")
    documentoUsuario = db.Column(db.String(30), nullable=False, unique=True)
    correoUsuario = db.Column(db.String(56), nullable=False, unique=True)
    telefonoUsuario = db.Column(db.String(60), unique=True)
    idRol = db.Column(
        db.Integer, db.ForeignKey("roles.idRol"), nullable=False, default=1
    )
    rolUsuario = db.relationship("Rol")
    descripcionUsuario = db.Column(db.String(255))
    fotoUsuario = db.Column(db.String(60))
    idEstado = db.Column(
        db.Integer, db.ForeignKey("estados.idEstado"), nullable=False, default=1
    )
    estadoUsuario = db.relationship("Estado")
    idVoto = db.Column(db.Integer, db.ForeignKey("usuarios.idUsuario"))
    votoUsuario = db.relationship("Usuario", remote_side=[idUsuario])
    contraseniaUsuario = db.Column(db.VARBINARY(256))
    codigoUsuario = db.Column(db.String(10))

    def get_id(self):
        return self.idUsuario
