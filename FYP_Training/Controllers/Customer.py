from flask import request,jsonify
from sqlalchemy import text
from FYP_Training.Model1.Customers import Customers
from FYP_Training.db import db

class CustomerController:
	@staticmethod
	def register():
		data=request.get_json()
		# val = Customer.query.get(email==email).all()
		# val = Customer.query.filter_by(email=mail)
		# if val is None:
		print('name=',data['name'], 'email=',data['email'], 'password=',data['password'])
		new_customer = Customers(name=data['name'], email=data['email'], password=data['password'])
		db.session.add(new_customer)
		db.session.commit()
		return jsonify({'msg': 'Data Add Successfully'})
		# else:
		# 	return jsonify({'msg': 'Email already exists'})
	# def register():
	# 	data = request.get_json()
	#
	# 	if not data or not all(k in data for k in ("name", "email", "password")):
	# 		return jsonify({'msg': 'Missing required fields'}), 400
	#
	# 	# Check if email already exists
	# 	existing = Customer.query.filter_by(email=data['email']).first()
	# 	if existing:
	# 		return jsonify({'msg': 'Email already exists'}), 409
	#
	# 	new_customer = Customer(
	# 		name=data['name'],
	# 		email=data['email'],
	# 		password=data['password']  # Storing plain password (not recommended)
	# 	)
	#
	# 	db.session.add(new_customer)
	# 	db.session.commit()
	#
	# 	return jsonify({'msg': 'Data added successfully', 'customer_id': new_customer.id}), 201
	@staticmethod
	def get_profile():
		cust = Customer.query.all()
		return jsonify([{'Id' : p.id,'Name': p.name, 'email': p.email} for p in cust])

	@staticmethod
	def update_profile(mail,pas,name):
		val = Customer.query.filter_by(email=mail).first()
		if val is not None:
			if val.password is pas:
				val.name=name
				db.session.commit()
				return jsonify({'msg': 'Successfully change name'})
			else:
				return jsonify({'msg': 'Wrong Password'})
		else:
			return jsonify({'msg': 'Email not exists'})

	@staticmethod
	def change_password(mail,pas,newpas):
		val = Customer.query.filter_by(email=mail).first()
		if val is not None:
			if val.password is pas:
				val.password = newpas
				db.session.commit()
				return jsonify({'msg': 'Successfully change Password'})
			else:
				return jsonify({'msg': 'Wrong Password'})
		else:
			return jsonify({'msg': 'Email not exists'})

	@staticmethod
	def delete_account(mail,pas):
		val = Customer.query.filter_by(email=mail).first()
		if val is not None:
			if val.password is pas:
				db.session.delete(val)
				db.session.commit()
				return jsonify({'msg': 'Successfully Deleted'})
			else:
				return jsonify({'msg': 'Wrong Password'})
		else:
			return jsonify({'msg': 'Email not exists'})

	@staticmethod
	def get_order_history():
		query = db.execute(text("""
		SELECT o.id AS order_id,
		       o.created_at,
		       o.total_price,
		       o.status,
		       p.name AS product_name,
		       oi.quantity,
		       oi.price_at_purchase
		FROM order o JOIN order_item oi ON o.id = oi.order_id JOIN product p ON oi.product_id = p.id
		WHERE o.customer_id = :result['id'] ORDER BY o.created_at DESC"""))
		return 	jsonify({'order_id':p.order_id,'product_name':p.product_name,'quantity':p.quantity,
						   'price_at_purchase':p.price_at_purchase,'total_price':p.total_price,'create_at':p.created_at,'status':p.status} for p in query)

	# def addCustomer():
	#     data=request.get_json()
	#     cust=Customer(name=data['name'],email=data['email'])
	#     db.session.add(cust)
	#     db.session.commit()
	#     return jsonify({'msg': 'Added Successfully'})