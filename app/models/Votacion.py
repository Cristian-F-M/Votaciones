from app import db

class Votacion(db.Model):
    
    __tablename__ = 'votaciones'

    idVotacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fechaInicioVotacion = db.Column(db.Date, nullable=False)
    fechaFinVotacion = db.Column(db.Date, nullable=False)
    ganadorVotacion = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    ganador = db.relationship('Usuario')
    cantVotosVotacion = db.Column(db.Integer, nullable=False)
    estadoVotacion_id = db.Column(db.Integer, db.ForeignKey('estados.idEstado'))
    estadoVotacion = db.relationship('Estado', backref='votaciones', foreign_keys=[estadoVotacion_id])

    
    
    def to_dict(self):
        return {
            'idVotacion': self.idVotacion,
            'fechaInicioVotacion': self.fechaInicioVotacion,
            'fechaFinVotacion': self.fechaFinVotacion,
            'ganadorVotacion': self.ganadorVotacion,
            'cantVotosVotacion': self.cantVotosVotacion,
            'estadoVotacion': self.estadoVotacion,
        }