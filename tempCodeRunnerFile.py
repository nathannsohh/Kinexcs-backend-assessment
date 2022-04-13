from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy import ForeignKey

DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "P@ssw0rd123"
DATABASE = "kinexcs"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/{DATABASE}'
db = SQLAlchemy(app)
api = Api(app)

class CustomerModel(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    def __repr__(self) -> str:
        return f"customer(id={id}, name={name}, dob={dob}"

class CustomerOrderModel(db.Model):
    __tablename__ = "customer_order"
    order_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable = False)
    item_price = db.Column(db.REAL, nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))

    def __repr__(self) -> str:
        return f"customer_order(order_id = {order_id}, item_name = {item_name}, item_price = {item_price}, date_time = {date_time}, customer_id = {customer_id}"


if __name__ == "__main__":
    app.run(debug=True)