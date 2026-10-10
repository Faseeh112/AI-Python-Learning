from datetime import datetime
from FYP_Training.db import db,Model
class Customer(db.Model):
    __tablename__ ='customer'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    cart_rship=db.relationship('Cart',back_populates='cus_rship')
    order_rship = db.relationship('Order', back_populates='cus_rship')
# from datetime import datetime
#
# from FYP_Training.db import db, Model
#
# class Customer(Model):
#     __tablename__ = 'customer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(100))
#     created_at = db.Column(db.DateTime, default=datetime.now)
#
#
# #
#     cart_rship = db.relationship("Cart", back_populates="cus_rship", uselist=False)
# from FYP_Training.db import db, Model
#
# class Customer(Model):
#     __tablename__ = 'customer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#
#     order_rship = db.relationship('Order', back_populates='cus_rship', cascade="all, delete-orphan")
