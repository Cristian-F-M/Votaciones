from app import db


class Estado(db.Model):
    __tablename__ = "estados"

    idEstado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcionEstado = db.Column(db.String(50), nullable=False)
