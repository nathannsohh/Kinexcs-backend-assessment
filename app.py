from json import loads
from flask import Flask, jsonify, request, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields
from sqlalchemy import ForeignKey

DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE = "kinexcs"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/{DATABASE}'
app.debug = True
db = SQLAlchemy(app)

class CustomerModel(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    def __init__(self, id, name, dob) -> None:
        self.id = id
        self.name = name
        self.dob = dob

    def __repr__(self) -> str:
        return f"customer(id={self.id}, name={self.name}, dob={self.dob})"

class CustomerSchema(Schema):
    id = fields.Integer(required = True)
    name = fields.String(required = True)
    dob = fields.Date(required = True)

class CustomerOrderModel(db.Model):
    __tablename__ = "customer_order"
    order_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable = False)
    item_price = db.Column(db.REAL, nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))

    def __init__(self, order_id, item_name, item_price, date_time, customer_id) -> None:
        self.order_id = order_id
        self.item_name = item_name
        self.item_price = item_price
        self.date_time = date_time
        self.customer_id = customer_id

    def __repr__(self) -> str:
        return f"customer_order(order_id = {self.order_id}, item_name = {self.item_name}, item_price = {self.item_price}, date_time = {self.date_time}, customer_id = {self.customer_id})"

class CustomerOrderSchema(Schema):
    order_id = fields.Integer()
    item_name = fields.String()
    item_price = fields.Float()
    date_time = fields.DateTime()
    customer_id = fields.Integer(required = True)

@app.route('/customer', methods = ['GET'])
def getCustomer():
    if 'number' in request.args:

        # Error Handling: Check if URL parameter for /customer?number=n is valid
        try:
            youngestN = int(request.args['number'])
        except ValueError:
            jsonMessage = jsonify(error=400, message=f"Bad Request: URL Parameter number = {request.args['number']} is not valid. URL parameter must be an integer.")
            response = make_response(jsonMessage, 400)
            abort(response)
        customerData = CustomerModel.query.order_by(CustomerModel.dob.desc()).limit(youngestN)
    else:
        customerData = CustomerModel.query.all()

    serializer = CustomerSchema(many = True)
    data = serializer.dump(customerData)
    return jsonify(data), 200

@app.route('/order', methods = ['GET'])
def getOrder():
    if 'customer_id' in request.args:

        # Error Handling: Check if URL parameter for /order?customer_id=x is valid 
        try:
            id = int(request.args['customer_id'])
        except ValueError:
            jsonMessage = jsonify(error=400, message=f"Bad Request: URL Parameter customer_id = {request.args['customer_id']} is not valid. URL parameter must be an integer.")
            response = make_response(jsonMessage, 400)
            abort(response)
        orderData = CustomerOrderModel.query.filter_by(customer_id = id).all()

        # Error Handling: Returns status 400 when requested id not in the database
        if len(orderData) == 0:
            jsonMessage = jsonify(error=404, message=f"customer_id {id} not found")
            response = make_response(jsonMessage, 404)
            abort(response)
    else:
        orderData = CustomerOrderModel.query.all()

    serializer = CustomerOrderSchema(many = True)
    data = serializer.dump(orderData)
    return jsonify(data), 200

@app.route('/customer/create', methods = ['POST'])
def createCustomer():

    # Error Handling: Returns status 400 if JSON cannot be decoded
    try:
        loads(request.data)
    except ValueError:
        jsonMessage = jsonify(error=400, message=f"Bad Request: Failed to decode JSON input. Please check the formatting of the JSON input.")
        response = make_response(jsonMessage, 400)
        abort(response)
    
    customerData = request.get_json()
    serializer = CustomerSchema()

    # Error Handling: Returns status 400 if input data not in corect format
    try:
        check = serializer.load(customerData)
    except ValidationError:
        jsonMessage = jsonify(error=400, message=f"Bad Request: Validation for inputs failed. Please check the format of the data inputted.")
        response = make_response(jsonMessage, 400)
        abort(response)
    
    custCheck = CustomerModel.query.filter_by(id = customerData.get('id')).all()
        
    # Error Handling: Customer id already exists in the database
    if len(custCheck) > 0:
        jsonMessage = jsonify(error=400, message=f"customer_id {customerData.get('id')} already exists, please use another id")
        response = make_response(jsonMessage, 400)
        abort(response)
    else:
        cust = CustomerModel(
            id = customerData.get('id'), 
            name = customerData.get('name'), 
            dob = customerData.get('dob')
        )

        db.session.add(cust)
        db.session.commit()

        data = serializer.dump(cust) 
        return jsonify(code=201, message="Data added successfully.", customer=data), 201

@app.errorhandler(500)
def internal_server(error):
    '''Return a 500 http status code'''
    return make_response(jsonify({"message":"There is a problem with the server, please try again later."}), 500)

@app.errorhandler(404)
def url_not_found(error):
    '''Return a 404 http status code'''
    return make_response(jsonify({"error" : 404, "message" : "Not Found: Invalid endpoint"}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    '''Return a 405 http status code'''
    return make_response(jsonify({"error" : 405, "message" : "Method Not Allowed: Please use the correct method for the requested URL."}), 405)

if __name__ == "__main__":
    app.run(debug=True)

