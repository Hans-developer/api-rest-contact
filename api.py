from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contact.db"
db = SQLAlchemy(app)

#crear modelo de base de datos

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable = False)

    #combertir a diccionario
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'fone': self.phone
        }
    



# crear las tablas en la base de datos
with app.app_context():
    db.create_all()


#crear rutas

# listar contactos
@app.route("/contact", methods=['GET'])
def get_contact():
    contacts = Contact.query.all()
    return jsonify({'contact': [cont.serialize() for cont in contacts]})


# agregar contacto
@app.route("/contact", methods=['POST'])
def create_contact():
    data = request.get_json()
    contact = Contact(name = data['name'],email = data['email'], phone = data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'mensage': 'creado con exito', 'contact': contact.serialize()})

# buscar contacto por id
@app.route("/contact/<int:id>", methods=['GET'])
def edit_contac(id):
    contacts = Contact.query.get(id)
    if not contacts:
        return jsonify({"mesage": 'Contacto no encontrado'}), 404
    return jsonify(contacts.serialize())

# editar contacto
@app.route("/contact/<int:id>", methods=['PUT', 'PATCH'])
def get_contac(id):
    contacts = Contact.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        contacts.name = data['name']
    if 'email' in data:
        contacts.email = data['email']
    if 'phone' in data:
        contacts.phone = data['phone']

    # guardar los cambios 
    db.session.commit()

    return jsonify({'mensage': 'actualizado con exito', 'contact': contacts.serialize()}), 201
    

# eliminar contacto
@app.route("/contact/<int:id>", methods=['DELETE'])
def delete_contac(id):
    contacts = Contact.query.get(id)
    if not contacts:
        return jsonify({"mesage": 'Contacto no encontrado'}), 404
    db.session.delete(contacts)
    db.session.commit()
    return jsonify({'message': 'Contacto eliminado con exito'})



if __name__ == '__main__':
    app.run(debug=True)