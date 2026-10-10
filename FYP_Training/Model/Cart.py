from FYP_Training.db import db,Model
class Cart(db.Model):
    __tablename__='cart'
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey("customer.id"))
    cus_rship=db.relationship('Customer',back_populates='cart_rship')
    cart_rship=db.relationship('CartItem',back_populates='cart_rship')
# from FYP_Training.db import db, Model
#
# class Cart(Model):
#     __tablename__ = 'cart'
#
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'))
#     cus_rship = db.relationship('Customer', back_populates='cart_rship')


# from FYP_Training.db import db, Model
#
# class Cart(Model):
#     __tablename__ = 'cart'
#     id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
#
#     cus_rship = db.relationship("Customer", back_populates="cart_rship")
#     cart_rship = db.relationship("CartItem", back_populates="cart_rship", cascade="all, delete-orphan")
