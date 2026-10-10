from FYP_Training.Model.OrderItem import OrderItem
from FYP_Training.Model.Order import Order
from FYP_Training.Model.Cart import Cart
from flask import render_template
from FYP_Training.Model.CartItem import CartItem
from flask import request, jsonify, session
from FYP_Training.Model1.Products import Products
from FYP_Training.Model1.Customers import Customers
from FYP_Training.db import db
from sqlalchemy import func

class ProductController:
	@staticmethod
	def showcart(id):
		print(id)
		result=db.session.query(CartItem.id,Product.name,Product.price,CartItem.quantity).join (Product,CartItem.product_id==Product.id).filter(CartItem.cart_id==id).all()
		result_json=[{"name":r.name,"price":r.price,"Quantity":r.quantity,"Total_Price":r.quantity*r.price} for r in result]
		return jsonify({"cart_id":id,'product':result_json})

	@staticmethod
	def viewcart(id):
		name = db.session.query(Customer.name).join(Cart, Cart.customer_id == Customer.id).filter(Cart.id == id).all()
		result = db.session.query(CartItem.id, Product.name, Product.price, CartItem.quantity).join(Product,CartItem.product_id == Product.id).filter(CartItem.cart_id == id).all()
		# result_json = [{"name": r.name, "price": r.price, "Quantity": r.quantity, "Total_Price": r.quantity * r.price}for r in result]
		# return jsonify({"cart_id": id, 'product': result_json})
		i=[+(r.quantity*r.price) for r in result]
		j=0
		print(i)
		for k in i:
			j=j+k
		print(i)
		print(result)
		return render_template("index.html", data=result,id=id,sum=j,name=name[0][0])

	@staticmethod
	def cart_all(id):
		name = db.session.query(Customer.name).join(Cart,Cart.customer_id == Customer.id).filter(Cart.id == id).all()
		result = db.session.query(CartItem.id, Product.name, Product.price, CartItem.quantity).join(Product,CartItem.product_id == Product.id).filter(CartItem.cart_id == id).all()
		result_json = [{"name": r.name, "price": r.price, "Quantity": r.quantity, "Total_Price": r.quantity * r.price} for r in result]
		return jsonify({"cart_id": id,"Customer_name":name[0][0], 'product': result_json})

	@staticmethod
	def count3():
		# val=db.session.query(CartItem.cart_id,Customer.name,func.count(CartItem.cart_id)).join(Cart,func.count(CartItem.cart_id)>3).join(Customer,Customer.id==Cart.customer_id).all()
		val = db.session.query(Cart.id.label("id"),Customer.name.label('name'),func.count(CartItem.cart_id).label("Cont")).join(Customer,Cart.customer_id==Customer.id).join(CartItem,CartItem.cart_id==Cart.id).group_by(Cart.id, Customer.name).having(func.count(CartItem.cart_id)>=3).all()
		return jsonify([{"Cart_id":v.id,"Customer name":v.name,"Products_Purchase":v.Cont} for v in val])

	# @staticmethod
	# def GetAllProduct():
	# 	prod = Product.query.all()
	# 	return jsonify([{'Name': p.name,'Description':p.description, 'Price': p.price, 'Stock': p.stock,'Category':p.category,'Img_url':p.img_url} for p in pr od])
	#
	# @staticmethod
	# def GetProductById(id):
	# 	p = Product.query.get(id)
	# 	if p is not None:
	# 		return jsonify({'Name': p.name,'Description':p.description, 'Price': p.price, 'Stock': p.stock,'Category':p.category,'Img_url':p.img_url})
	# 	else:
	# 		return jsonify({'msg': 'Product not found'})
	#
	# @staticmethod
	# def AddProduct():
	# 	data = request.get_json()
	# 	prod = Product(name=data['name'], price=data['price'],stock=data['stock'],category=data['category'],description=data['description'],img_url=data['img_url'])
	# 	db.session.add(prod)
	# 	db.session.commit()
	# 	return jsonify({'msg': 'Added Successfully'})
	#
	# @staticmethod
	# def update_product():
	# 	data=request.get_json()
	# 	val = Product.query.filter_by(id=data['id']).first()
	# 	if data:
	# 		val.name=data['name']
	# 		val.description=data['description']
	# 		val.price=data['price']
	# 		val.stock = data['stock']
	# 		val.category = data['category']
	# 		val.img_url = data['img_url']
	# 		db.session.commit()
	# 		return jsonify({'msg': 'Updated Successfully'})
	# 	else:
	# 		return jsonify({'msg': 'Id not found'})
	#
	# @staticmethod
	# def delete_product():
	# 	data = request.get_json()
	# 	val = Product.query.filter_by(id=data['id']).first()
	# 	if id:
	# 		db.session.delete(val)
	# 		db.session.commit()
	# 		return jsonify({'msg': 'Deleted Successfully'})
	# 	else:
	# 		return jsonify({'msg': 'Id not found'})
	#
	# @staticmethod
	# def search_products():
	# 	data=request.get_json()
	# 	p = Product.query.filter_by(name=data['name']).first()
	# 	if p:
	# 		return jsonify({'Name': p.name,'Description':p.description, 'Price': p.price, 'Stock': p.stock,'Category':p.category,'Img_url':p.img_url})
	# 	else:
	# 		return jsonify({'msg': 'Product not found'})
	#
	# @staticmethod
	# def filter_by_category():
	# 	data=request.get_json()
	# 	prod = Product.query.filter_by(category=data['category']).first()
	# 	return jsonify([{'Name': p.name, 'Description': p.description, 'Price': p.price, 'Stock': p.stock,'Category': p.category, 'Img_url': p.img_url} for p in prod])
	#
	# def add_to_cart(customer_id, product_id, quantity):
	# 	try:
	# 		cart = Cart.query.filter_by(customer_id=customer_id).first()
	# 		if not cart:
	# 			cart = Cart(customer_id=customer_id)
	# 			db.session.add(cart)
	# 			db.session.commit()
	# 		product = Product.query.get(product_id)
	# 		if not product or product.stock < quantity:
	# 			return {"error": "Product not found or insufficient stock"}, 400
	# 		cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
	# 		if cart_item:
	# 			cart_item.quantity += quantity
	# 		else:
	# 			cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
	# 			db.session.add(cart_item)
	# 		product.stock -= quantity
	# 		db.session.commit()
	# 		return {"message": "Added to cart"}
	# 	except Exception as e:
	# 		db.session.rollback()
	# 		return {"error": str(e)}, 400
	#
	# def view_cart(customer_id):
	# 	cart = Cart.query.filter_by(customer_id=customer_id).first()
	# 	if cart:
	# 		return [{
	# 			"id": item.id,
	# 			"product_id": item.product_id,
	# 			"product_name": item.product.name,
	# 			"quantity": item.quantity,
	# 			"description": item.product.description,
	# 			"category": item.product.category,
	# 			"price": item.product.price
	# 		} for item in cart.items]
	# 	return []
	#
	# def update_cart_item(item_id, quantity):
	# 	cart_item = CartItem.query.get(item_id)
	# 	if cart_item:
	# 		product = Product.query.get(cart_item.product_id)
	# 		stock_diff = quantity - cart_item.quantity
	# 		if product.stock >= stock_diff:
	# 			cart_item.quantity = quantity
	# 			product.stock -= stock_diff
	# 			db.session.commit()
	# 			return {"message": "Cart item updated"}
	# 		return {"error": "Insufficient stock"}, 400
	# 	return {"error": "Cart item not found"}, 404
	#
	# def remove_cart_item(item_id):
	# 	cart_item = CartItem.query.get(item_id)
	# 	if cart_item:
	# 		product = Product.query.get(cart_item.product_id)
	# 		product.stock += cart_item.quantity
	# 		db.session.delete(cart_item)
	# 		db.session.commit()
	# 		return {"message": "Cart item removed"}
	# 	return {"error": "Cart item not found"}, 404
	#
	# def clear_cart(customer_id):
	# 	cart = Cart.query.filter_by(customer_id=customer_id).first()
	# 	if cart:
	# 		for item in cart.items:
	# 			product = Product.query.get(item.product_id)
	# 			product.stock += item.quantity
	# 		CartItem.query.filter_by(cart_id=cart.id).delete()
	# 		db.session.commit()
	# 		return {"message": "Cart cleared"}
	# 	return {"error": "Cart not found"}, 404
	#
	# def checkout_order(customer_id):
	# 	try:
	# 		cart = Cart.query.filter_by(customer_id=customer_id).first()
	# 		if not cart or not cart.items:
	# 			return {"error": "Cart is empty"}, 400
	# 		total_price = sum(item.product.price * item.quantity for item in cart.items)
	# 		order = Order(customer_id=customer_id, total_price=total_price)
	# 		db.session.add(order)
	# 		db.session.commit()
	# 		for item in cart.items:
	# 			order_item = OrderItem(
	# 				order_id=order.id,
	# 				product_id=item.product_id,
	# 				quantity=item.quantity,
	# 				price_at_purchase=item.product.price
	# 			)
	# 			db.session.add(order_item)
	# 		CartItem.query.filter_by(cart_id=cart.id).delete()
	# 		db.session.commit()
	# 		return {"message": "Order placed", "order_id": order.id}
	# 	except Exception as e:
	# 		db.session.rollback()
	# 		return {"error": str(e)}, 400
	#
	# def get_orders(customer_id):
	# 	return Order.query.filter_by(customer_id=customer_id).all()
	#
	# def get_order_by_id(order_id):
	# 	return Order.query.get(order_id)
	#
	# def cancel_order(order_id):
	# 	order = Order.query.get(order_id)
	# 	if order and order.status == 'pending':
	# 		order.status = 'cancelled'
	# 		for item in order.items:
	# 			product = Product.query.get(item.product_id)
	# 			product.stock += item.quantity
	# 		db.session.commit()
	# 		return {"message": "Order cancelled"}
	# 	return {"error": "Order not found or cannot be cancelled"}, 404
	#
	# def get_cart_item(item_id):
	# 	return CartItem.query.get(item_id)