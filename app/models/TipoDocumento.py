
from app import db

class TipoDocumento(db.Model):

    __tablename__ = 'tiposdocumento'

    idTipoDocumento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcionTipoDocumento = db.Column(db.String(45), nullable=False)


    def to_dict(self):
        return {
            'idTipoDocumento': self.idTipoDocumento,
            'descripcionTipoDocumento': self.descripcionTipoDocumento
        }
