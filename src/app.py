from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Finca(db.Model):
    nit = db.Column(db.String(20), primary_key = True, unique = True)
    nombre  = db.Column(db.String(20))
    contacto  = db.Column(db.String(20))
    direccion = db.Column(db.String(20))
    correo  = db.Column(db.String(20))
    propietario = db.Column(db.String(20))

    def __init__(self, nit, nombre,contacto, direccion, correo , propietario) :
        self.nit = nit
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
        self.correo = correo
        self.propietario = propietario

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    numero = db.Column(db.String(20))
    nit_finca = db.Column(db.String(20))
    responsable = db.Column(db.String(20))
    cultivo = db.Column(db.String(20))
    existencias = db.Column(db.Integer)

    def __init__(self, id, numero, nit_finca,responsable , cultivo,existencias ) :
        self.id = id
        self.numero = numero
        self.nit_finca = nit_finca
        self.responsable = responsable
        self.cultivo = cultivo
        self.existencias = existencias

    def serialize(self):
        return {
        "id" : self.id ,
        "numero" : self.numero,
        "nit_finca" : self.nit_finca,
        "responsable" : self.responsable,
        "cultivo" : self.cultivo,
        "existencias" : self.existencias,
        }


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    nit_finca = db.Column(db.String(20))
    id_Lote = db.Column(db.Integer)
    cantidad_Compra = db.Column(db.Integer)

    def __init__(self, id, nit_finca,id_Lote, cantidad_Compra  ) :
        self.id = id
        self.nit_finca = nit_finca
        self.id_Lote = id_Lote
        self.cantidad_Compra = cantidad_Compra


with app.app_context():
    db.create_all()


class FincaSchema(ma.Schema):
    class Meta:
        fields = ("nit","nombre","contacto","direccion","correo","propietario")

class LoteSchema(ma.Schema):
    class Meta:
        fields = ("id","numero","nit_finca","responsable","cultivo","existencias")

class VentaSchema(ma.Schema):
    class Meta:
        fields = ("id","nit_finca","id_Lote","cantidad_Compra")



finca_schema = FincaSchema()
fincas_schema = FincaSchema(many=True)

lote_schema = LoteSchema()
lotes_schema = LoteSchema(many=True)

venta_schema = VentaSchema()
ventas_schema = VentaSchema(many=True)



# Rutas Finca
@app.route('/finca' , methods=['POST'])
def create_finca():
    nit = request.json["nit"]
    nombre = request.json["nombre"]
    contacto = request.json["contacto"]
    direccion = request.json["direccion"]
    correo = request.json["correo"]
    propietario = request.json["propietario"]

    new_Finca = Finca(nit,nombre,contacto,direccion,correo,propietario)
    db.session.add(new_Finca)
    db.session.commit()


    return finca_schema.jsonify(new_Finca)

@app.route('/fincas', methods=['GET'])
def getFincas():
    all_Fincas = Finca.query.all()
    result = fincas_schema.dump(all_Fincas)
    
    return jsonify(result)

@app.route('/finca/<nit>', methods=['GET'])
def getFinca(nit):
    finca = Finca.query.get(nit)

    return finca_schema.jsonify(finca)

@app.route('/finca/<nit>', methods=['PUT'])
def updateFinca(nit):

    finca = Finca.query.get(nit)

    nombre = request.json["nombre"]
    contacto = request.json["contacto"]
    direccion = request.json["direccion"]
    correo = request.json["correo"]
    propietario = request.json["propietario"]

    finca.nombre = nombre
    finca.contacto = contacto
    finca.direccion = direccion
    finca.correo = correo
    finca.propietario = propietario

    db.session.commit()

    return finca_schema.jsonify(finca)

@app.route('/finca/<nit>', methods=['DELETE'])
def deteleFinca(nit):
   finca = Finca.query.get(nit)

   db.session.delete(finca)
   db.session.commit()

   return finca_schema.jsonify(finca)


# Rutas Lote
@app.route('/lote' , methods=['POST'])
def create_lote():
    
    id = request.json["id"]
    numero = request.json["numero"]
    nit_finca = request.json["nit_finca"]
    responsable = request.json["responsable"]
    cultivo = request.json["cultivo"]
    existencias = request.json["existencias"]

    finca = Finca.query.get(nit_finca)

    if(finca):
            new_Lote = Lote(id,numero,nit_finca,responsable,cultivo,existencias)
            db.session.add(new_Lote)
            db.session.commit()
            return lote_schema.jsonify(new_Lote)
    else:
        return "El NIT de la finca Asignada no es valido o no existe: " +  nit_finca
    
@app.route('/lotes', methods=['GET'])
def getLotes():
    all_Lotes = Lote.query.all()
    result = lotes_schema.dump(all_Lotes)
    
    return jsonify(result)

@app.route('/lote/<id>', methods=['GET'])
def getLote(id):
    lote = Lote.query.get(id)

    return lote_schema.jsonify(lote)

@app.route('/lote/<id>', methods=['PUT'])
def updateLote(id):
    lote = Lote.query.get(id)

    numero = request.json["numero"]
    nit_finca = request.json["nit_finca"]
    responsable = request.json["responsable"]
    cultivo = request.json["cultivo"]
    existencias = request.json["existencias"]

    lote.numero = numero
    lote.nit_finca = nit_finca
    lote.responsable = responsable
    lote.cultivo = cultivo
    lote.existencias = existencias

    db.session.commit()

    return lote_schema.jsonify(lote)

@app.route('/lote/<id>', methods=['DELETE'])
def deteleLote(id):
    lote = Lote.query.get(id)

    db.session.delete(lote)
    db.session.commit()

    return lote_schema.jsonify(lote)


# Rutas Combinadas
@app.route('/Inventario/<nit>', methods=['GET'])
def getInventario(nit):

    finca = Finca.query.get(nit)

    if(finca):
        lotes = Lote.query.filter_by(nit_finca=nit).all()
        # Retorna los lotes correspondientes en formato JSON
        return jsonify([lote.serialize() for lote in lotes])
    else:
        return "Esta Finca no existe"
    

# Ruta Ventas
@app.route('/venta' , methods=['POST'])
def create_venta():
    id = request.json["id"]
    nit_finca = request.json["nit_finca"]
    id_Lote = request.json["id_Lote"]
    cantidad_Compra = request.json["cantidad_Compra"]

    finca = Finca.query.get(nit_finca)
    lote = Lote.query.get(id_Lote)
    if(finca):
            if(lote):
                if(finca.nit == lote.nit_finca):
                    if(cantidad_Compra > 0):
                        lotecantidaddispo =  lote.existencias - cantidad_Compra
                        if( lotecantidaddispo >= 0):
                            lote.existencias = lote.existencias - cantidad_Compra
                            db.session.commit()
                            new_venta = Venta(id,nit_finca,id_Lote,cantidad_Compra)
                            db.session.add(new_venta)
                            db.session.commit()
                            return venta_schema.jsonify(new_venta)
                        else:
                            return "El lote no tiene la cantidad disponible para la venta" 
                    else:
                        return "La cantidad a comprar debe ser mayor a 0"
                else:
                    return "El lote no pertenece a la Finca ingresada"
            else:
                return "El Numero del Lote no es valido o no existe: " + id_Lote
    else:
        return "El NIT de la finca Asignada no es valido o no existe: " +  nit_finca



if __name__ == "__main__":
    app.run(debug=True)
