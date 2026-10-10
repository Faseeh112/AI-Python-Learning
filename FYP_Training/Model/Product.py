from FYP_Training.db import db,Model
class Product(Model):
    __tablename__='product'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price=db.Column(db.Integer,nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category=db.Column(db.String(100),nullable=False)
    img_url=db.Column(db.String(100),nullable=False)
    cart_rship=db.relationship('CartItem',back_populates='pro_rship')
    order_rship = db.relationship('OrderItem', back_populates='pro_rship')
#
# from FYP_Training.db import db, Model
#
# class Product(Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     price = db.Column(db.Float)
#     stock = db.Column(db.Integer)
#     category = db.Column(db.String(50))
#     description = db.Column(db.Text)
#     img_url = db.Column(db.String(255))
#
#     cart_rship = db.relationship("CartItem", back_populates="pro_rship", cascade="all, delete-orphan")


# from FYP_Training.db import db, Model
#
# class Product(Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     price = db.Column(db.Float)
#     stock = db.Column(db.Integer)
#     category = db.Column(db.String(50))
#     description = db.Column(db.Text)
#     img_url = db.Column(db.String(255))
#
#     cart_rship = db.relationship('CartItem', back_populates='pro_rship', cascade='all, delete-orphan')
#     order_rship = db.relationship('OrderItem', back_populates='pro_rship', cascade='all, delete-orphan')
