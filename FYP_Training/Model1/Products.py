from FYP_Training.db import db,Model
class Products(Model):
	__tablename__='products'
	product_ID=db.Column(db.Integer,primary_key=True)
	product_type=db.Column(db.String(100),nullable=False)
	product_name=db.Column(db.String(100),nullable=False)
	size=db.Column(db.String(100),nullable=False)
	colour=db.Column(db.String(100),nullable=False)
	price=db.Column(db.Integer, nullable=False)
	quantity=db.Column(db.Integer, nullable=False)
	description=db.Column(db.String(100),nullable=False)
	sale_re = db.relationship('Sales', back_populates='prod_re')