from app import db


class Voto(db.Model):
    __tablename__ = "voto"

    idVoto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"))
    candidato = db.relationship("Usuario", backref="voto")
    fechaVoto = db.Column(db.TIMESTAMP, nullable=False)
