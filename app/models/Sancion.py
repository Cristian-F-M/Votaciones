from sqlalchemy import func
from app import db


class Sancion(db.Model):
    __tablename__ = "sanciones"

    idSancion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(
        db.Integer, db.ForeignKey("usuarios.idUsuario"), nullable=False
    )
    usuario = db.relationship("Usuario")
    fechaSancion = db.Column(db.Date, default=func.now())
    motivoSancion = db.Column(db.String(100), nullable=False)
    detalleSancion = db.Column(db.String(250), default="N/A")
