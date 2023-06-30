from flask_sqlalchemy import SQLAlchemy
from enum import unique
from collections import UserList

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    cedula = db.Column(db.String(80), unique=True, nullable=(False))
    direccion= db.Column(db.String(120), unique=(False), nullable=(False))
    nombre_completo = db.Column(db.String(80), unique=(False), nullable=(False))
    # is_active = db.Column(db.Boolean, default=True)
    pedidos_id = db.relationship('Pedidos', backref ='user', uselist=True)
    tipo = db.Column(db.String(80),unique=False, nullable=False)
    salt = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "nombre completo": self.nombre_completo
            # do not serialize the password, its a security breach
        }

class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(20),unique=False, nullable=True)
    marca = db.Column(db.String(80), unique=False, nullable=True)
    año = db.Column(db.Integer, unique=False, nullable=True)
    serial = db.Column(db.String(20), unique=False, nullable=True)
    
    Detalle_piezas_pedidos  = db.relationship('Detalle', backref ='pedidos', uselist=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Pedidos {self.id}>'
    def serialize(self):
        return{
            "id":self.id,
            "modelo":self.modelo,
            "marca":self.marca,
            "año":self.año,
            "serial": self.serial,
            "user_id":self.user_id
            }

class Detalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pieza = db.Column(db.String(20), unique=False, nullable=True)
    cantidad = db.Column(db.String(8), unique=False, nullable=True)
    imagen = db.Column(db.String(200), unique=False, nullable=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))

    def __repr__(self):
        return f'<Detalle_piezas_pedidos {self.id}>'
    def serialize(self):
        return{
            "id":self.id, 
            "pieza":self.id,
            "cantidad":self.cantidad, 
            "imagen":self.imagen
        }