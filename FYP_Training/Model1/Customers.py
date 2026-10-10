from datetime import datetime
from FYP_Training.db import db,Model
class Customers(db.Model):
	__tablename__ ='customers'
	customer_id=db.Column(db.Integer,primary_key=True)
	customer_name=db.Column(db.String(100),nullable=False)
	gender=db.Column(db.String(50),nullable=False)
	age=db.Column(db.Integer,nullable=False)
	home_address=db.Column(db.String(100),nullable=False)
	zip_code=db.Column(db.Integer,nullable=False)
	city=db.Column(db.String(100),nullable=False)
	state=db.Column(db.String(100),nullable=False)
	country=db.Column(db.String(100),nullable=False)
	order_re= db.relationship('Orders', back_populates='cus_rs')