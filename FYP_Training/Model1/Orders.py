from datetime import datetime
from FYP_Training.db import db,Model
class Orders(Model):
	__tablename__='orders'
	order_id=db.Column(db.Integer,primary_key=True)
	customer_id=db.Column(db.Integer,db.ForeignKey("customers.customer_id"))
	payment=db.Column(db.Integer,nullable=False)
	order_date=db.Column(db.DateTime, default=datetime.now)
	delivery_date = db.Column(db.DateTime, default=datetime.now)
	cus_rs=db.relationship('Customers',back_populates='order_re')
	sale_re= db.relationship('Sales', back_populates='order_re')