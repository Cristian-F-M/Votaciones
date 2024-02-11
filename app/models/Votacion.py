from app import db

class Votacion(db.Model):
    
    __tablename__ = 'votaciones'

    idVotacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fechaInicioVotacion = db.Column(db.Date, nullable=False)
    fechaFinVotacion = db.Column(db.Date, nullable=False)
    idGanador = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=True)
    ganadorVotacion = db.relationship('Usuario')
    cantVotosVotacion = db.Column(db.Integer, nullable=True)
    porcentajeVotosVotacion = db.Column(db.String(10), nullable=True)
    totalVotosVotacion = db.Column(db.Integer, nullable=True)
    idEstado = db.Column(db.Integer, db.ForeignKey('estados.idEstado'), default=1)
    estadoVotacion = db.relationship('Estado', backref='votaciones')

