from datetime import datetime
from FYP_Training.db import db,Model
class Sales(Model):
	__tablename__='sales'
	sales_id=db.Column(db.Integer,primary_key=True)
	order_id=db.Column(db.Integer,db.ForeignKey("orders.order_id"))
	product_id=db.Column(db.Integer,db.ForeignKey("products.product_ID"))
	price_per_unit=db.Column(db.Integer,nullable=False)
	quantity=db.Column(db.Integer,nullable=False)
	total_price=db.Column(db.Integer,nullable=False)
	prod_re=db.relationship('Products',back_populates='sale_re')
	order_re=db.relationship('Orders',back_populates='sale_re')