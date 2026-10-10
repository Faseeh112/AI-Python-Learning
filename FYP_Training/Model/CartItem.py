from FYP_Training.db import db,Model
class CartItem(Model):
    __tablename__='cartItem'
    id=db.Column(db.Integer,primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    cart_rship=db.relationship('Cart',back_populates='cart_rship')
    pro_rship = db.relationship('Product', back_populates='cart_rship')

# from FYP_Training.db import db, Model
#
# class CartItem(Model):
#     __tablename__ = 'cartItem'
#     id = db.Column(db.Integer, primary_key=True)
#     cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
#     product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
#     quantity = db.Column(db.Integer, nullable=False)
#
#     cart_rship = db.relationship("Cart", back_populates="cart_rship")
#     pro_rship = db.relationship("Product", back_populates="cart_rship")
