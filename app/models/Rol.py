from app import db

class Rol(db.Model):
    __tablename__ = 'roles'

    idRol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcionRol = db.Column(db.String(45), nullable=False)

