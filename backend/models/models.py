from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer 
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

# tabla de usuarios
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    
    fotos = db.relationship('Foto', back_populates='usuario', cascade='all, delete-orphan')

# tabla de fotos
class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nobrefoto = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.LargeBinary (length= 16 * 1024 * 1024 ), nullable=False)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario',back_populates='fotos')

# tabla de diagnosticos
class Diagnostico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombrearchivo = db.Column(db.String(150), nullable=False)
    ruta = db.Column(db.String(120), nullable=False)
    predicion = db.Column(db.String(100), nullable=False)
    fecha= db.Column(db.Date, default=datetime.today)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    
    Usuario = db.relationship('Usuario', backref=db.backref('diagnosticos', lazy=True))
    
    
