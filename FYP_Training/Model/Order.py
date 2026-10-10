from datetime import datetime
from FYP_Training.db import db,Model
class Order(Model):
    __tablename__='order'
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey("customer.id"))
    total_price=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    order_rship = db.relationship('OrderItem', back_populates='order_rship')
    cus_rship = db.relationship('Customer', back_populates='order_rship')
# from datetime import datetime
# from FYP_Training.db import db, Model
#
# class Order(Model):
#     __tablename__ = 'order'
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
#     total_price = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(100), nullable=False, default='pending')
#     created_at = db.Column(db.DateTime, default=datetime.now)
#
#     order_rship = db.relationship('OrderItem', back_populates='order_rship', cascade="all, delete-orphan")
#     cus_rship = db.relationship('Customer', back_populates='order_rship')
