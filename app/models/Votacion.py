from app import db

class Votacion(db.Model):
    
    __tablename__ = 'votaciones'

    idVotacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fechaInicioVotacion = db.Column(db.Date, nullable=False)
    fechaFinVotacion = db.Column(db.Date, nullable=False)
    ganadorVotacion = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    ganador = db.relationship('Usuario')
    cantVotosVotacion = db.Column(db.Integer, nullable=True)
    porcentajeVotosVotacion = db.Column(db.String(10), nullable=True)
    totalVotosVotacion = db.Column(db.Integer, nullable=True)
    estadoVotacion = db.Column(db.Integer, db.ForeignKey('estados.idEstado'))
    estadoVotacionF = db.relationship('Estado', backref='votaciones')

