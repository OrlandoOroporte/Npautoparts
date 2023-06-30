"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import email
from ast import Try
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Pedidos, Detalle
from api.utils import generate_sitemap, APIException
from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity



api = Blueprint('api', __name__)

def set_password(password, salt):
    return generate_password_hash(f'{password}{salt}')

def check_password(hash_password, password, salt):
    return check_password_hash(hash_password,f'{password}{salt}')

@api.route('/user', methods=['POST'])
def add_user():
    body=request.json
    email=body.get('email',None)
    password=body.get('password', None)
    cedula=body.get('cedula',None)
    direccion=body.get('direccion',None)
    nombre_completo=body.get('nombre_completo', None)
    tipo=body.get('tipo', None)
    if len(email) < 1 or len(password)<1 or len(cedula)<1 or  len(direccion)<1 or len(nombre_completo)<1 or len(tipo)<1:
        return jsonify('Todos los campos excepto tipo son obligatorios')
    elif "@"  not in email or '.com' not in email: 
        return jsonify('Correo no valido')
    elif len(cedula) < 6 or len(cedula) > 8: 
        print('cedula no valida')
        return jsonify('Cedula no valida')
    else:
        salt= b64encode(os.urandom(32)).decode('utf-8')
        password= set_password(password, salt)
        request_user = User(email=email, password=password, cedula=cedula, direccion=direccion, nombre_completo=nombre_completo, tipo=tipo, salt=salt)
        db.session.add(request_user)

        try:
            db.session.commit()
            return jsonify('Su usuario ha sido registrado'),201
        except Exception as error:
            db.session.rollback()
            print(error.args)
            return jsonify(error.args),500 

@api.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.get('email', None)
    password = body.get('password', None)

    login_user = User.query.filter_by(email=email).first()
    if login_user:
        if check_password(login_user.password, password, login_user.salt):
            created_token = create_access_token(identity=login_user.id)
            return jsonify({ 'token': created_token}),200
        else: 
            return jsonify('Error en la clave')

        print(login_user)   
    else: 
        print("Usuario no exite")    
    
    return jsonify("Error en la clave"),200
    
@api.route('/pedidos', methods=['POST'])
@jwt_required()
def add_pedido():
    body= request.json
    marca = body.get('marca', None)
    modelo= body.get('modelo', None)
    año = body.get('año', None)
    serial = body.get('serial', None)

    user_id = get_jwt_identity()
    print(user_id)

    if len(marca) < 1 or len(modelo)<1 or len(año)<1 or len(serial)<1:
        print('Todos los campos son necesarios para el registro')
        return jsonify('Todos los campos son necesarios para el registro')
    elif len(año)!= 4:
        print('Año de vehiculo no valido')
        return jsonify('Año de vehiculo no valido')
    elif len(serial)!= 17:
        print('El serial no es valido')
        return jsonify('El serial no es valido')
    else: 
        request_pedido=Pedidos(marca=marca, modelo=modelo, año=año, serial=serial)
        db.session.add(request_pedido)

        try:
            db.session.commit()
            return jsonify('se ha grabado el pedido'),200
        except ExecError as error:
            db.session.rollback
            print(error.args)
            return jsonify(error.args),500 
            



# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200