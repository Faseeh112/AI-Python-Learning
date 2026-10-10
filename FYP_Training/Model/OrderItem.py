from FYP_Training.db import db,Model
class OrderItem(Model):
    __tablename__='orderItem'
    id=db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    Price_at_purchase = db.Column(db.Integer, nullable=False)
    order_rship=db.relationship('Order',back_populates='order_rship')
    pro_rship = db.relationship('Product', back_populates='order_rship')
# from FYP_Training.db import db, Model
#
# class OrderItem(Model):
#     __tablename__ = 'orderItem'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     quantity = db.Column(db.Integer, nullable=False)
#     price_at_purchase = db.Column(db.Integer, nullable=False)
#
#     order_rship = db.relationship('Order', back_populates='order_rship')
#     pro_rship = db.relationship('Product', back_populates='order_rship')
