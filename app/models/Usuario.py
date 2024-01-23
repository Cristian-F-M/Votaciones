from app import db, login_manager
from flask_login import UserMixin
from flask import session


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
    estadoUsuario = db.Column(
        db.Integer, db.ForeignKey("estados.idEstado"), nullable=False, default=1
    )
    idVoto = db.Column(db.Integer, db.ForeignKey("voto.idVoto"))
    votoUsuario = db.relationship("Voto", backref="usuario")
    contraseniaUsuario = db.Column(db.String(256))
    codigoUsuario = db.Column(db.String(10))

    def to_dict(self):
        return {
            "idUsuario": self.idUsuario,
            "nombreUsuario": self.nombreUsuario,
            "apellidoUsuario": self.apellidoUsuario,
            "idTipoDocumento": self.idTipoDocumento,
            "tipoDocumentoUsuario": self.tipoDocumentoUsuario,
            "documentoUsuario": self.documentoUsuario,
            "correoUsuario": self.correoUsuario,
            "telefonoUsuario": self.telefonoUsuario,
            "idRol": self.idRol,
            "rolUsuario": self.rolUsuario,
            "descripcionUsuario": self.descripcionUsuario,
            "fotoUsuario": self.fotoUsuario,
            "estadoUsuario": self.estadoUsuario,
            "idVoto": self.idVoto,
            "votoUsuario": self.votoUsuario,
            "codigo": self.codigo,
        }

    def get_id(self):
        return self.idUsuario


@login_manager.user_loader
def load_user(usuario):
    usuarioS = Usuario.query.get(int(usuario))
    print(usuarioS)
    return usuarioS
