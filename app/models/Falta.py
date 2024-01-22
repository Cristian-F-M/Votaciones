from app import db


class Falta(db.Model):
    __tablename__ = "faltas"

    idFalta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(
        db.Integer, db.ForeignKey("usuarios.idUsuario"), nullable=False
    )
    usuario = db.relationship("Usuario")
    fechaFalta = db.Column(db.TIMESTAMP, nullable=False)
    detalleFalta = db.Column(db.String(255), nullable=False, default="No hay detalle")

    def to_dict(self):
        return {
            "idFalta": self.idFalta,
            "idUsuario": self.idUsuario,
            "usuario": self.usuario,
            "fechaFalta": self.fechaFalta,
            "detalleFalta": self.detalleFalta,
        }
